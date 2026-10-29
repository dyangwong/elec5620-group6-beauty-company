"""Bounded natural exchange orchestration; inference never holds a DB connection."""
from copy import deepcopy
from functools import wraps
import json
import sqlite3

from ..adapters.cs_intent import validate_intent
from ..adapters.llm import ModelError
from ..contracts import DomainError, require_role, revision_value, text_value
from ..store import Store, new_id
from .beauty_advisor import catalogue, validated_needs
from .cs_evidence import require_same_policy


def storage_boundary(method):
    @wraps(method)
    def wrapped(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except sqlite3.Error:
            raise DomainError('The service work could not be recorded. Refresh the current request; '
                              'no saved result or completed action is claimed.', 503, 'CS_STORAGE_UNAVAILABLE') from None
    return wrapped


class CsFlow:
    def __init__(self, store, cs, llm):
        self.store, self.cs, self.llm = store, cs, llm

    @property
    def simulated(self):
        return getattr(self.llm, 'cs_simulated', getattr(self.llm, 'simulated', True))

    @staticmethod
    def identity(db, actor, role, authenticate):
        require_role(actor, role)
        if authenticate:
            current = authenticate()
            if (current.id, current.role) != (actor.id, actor.role):
                raise DomainError('The current identity changed. Sign in again.', 401, 'UNAUTHENTICATED')
        user = db.execute('SELECT role FROM users WHERE id=?', (actor.id,)).fetchone()
        if not user or user['role'] != role:
            raise DomainError('The current identity is no longer authorised.', 403, 'FORBIDDEN')

    def policy(self, db, record):
        _, policy = self.cs.eligible_order(db, record['owner_id'], record['payload']['orderId'])
        if record['payload'].get('policy'):
            require_same_policy(policy, record['payload']['policy'])
        return policy

    def blocked_policy(self, db, record, error):
        if record['payload'].get('naturalIntent'):
            record['payload']['naturalIntent']['stage'] = 'BLOCKED'
        return self.cs._blocked(db, record, error)

    @storage_boundary
    def start(self, actor, data, rid=None, authenticate=None):
        expected = {'message', 'contextRevision'} if rid else {'message', 'orderId'}
        if set(data) != expected:
            raise DomainError('Supply only the service message and order reference or current revision.')
        message = text_value(data.get('message'), 'Service request', 2000)
        revision = revision_value(data.get('contextRevision')) if rid else 1
        mode = self.simulated
        if type(mode) is not bool:
            raise DomainError('The service intent capability has invalid mode metadata.', 503, 'LLM_CAPABILITY_UNAVAILABLE')
        with self.store.transaction() as db:
            self.identity(db, actor, 'CUSTOMER', authenticate)
            if rid:
                record = self.cs.owned(db, actor, rid)
                if record['revision'] != revision:
                    raise DomainError('The request changed. Review the current revision.', 409, 'STALE_SCOPE')
                if record['status'] in {'EXECUTING', 'RECONCILING', 'RECORDING_FAILED', 'RESOLVED', 'CANCELLED'}:
                    raise DomainError('Resolve the existing action before changing this request.', 409, 'INVALID_STATE')
                # Verify association before replacing any saved scope; policy may be retained as blocked.
                from .cs_evidence import read_order
                read_order(self.cs.evidence, db, actor.id, record['payload']['orderId'])
                self.cs.ap.supersede(db, record['payload'].get('approvalId'))
                history = record['payload'].get('history', []) + [{'contextRevision': revision,
                    'status': record['status'], 'payload': {k: v for k, v in record['payload'].items() if k != 'history'}}]
                record['revision'] += 1
                record['payload'] = {'orderId': record['payload']['orderId'],
                    'coordinationId': record['payload']['coordinationId'], 'history': history, 'simulated': True}
            else:
                from .cs_evidence import read_order
                order_id = text_value(data.get('orderId'), 'Order reference', 100)
                read_order(self.cs.evidence, db, actor.id, order_id)
                for row in db.execute("SELECT id,payload,status FROM records WHERE kind='CS' AND owner_id=?", (actor.id,)):
                    payload = json.loads(row['payload'])
                    if payload.get('orderId') == order_id and row['status'] not in {'REJECTED', 'CANCELLED'}:
                        if payload.get('naturalIntent', {}).get('message') == message:
                            return Store.get(db, row['id'])  # idempotent intake; never new inference/effect
                        raise DomainError('An exchange already exists. Revise that request explicitly.', 409, 'DUPLICATE_REQUEST')
                rid = Store.create(db, 'CS', actor.id, 'ASSESSING', {'orderId': order_id, 'simulated': True}, 'CS')
                record = Store.get(db, rid)
                record['payload']['coordinationId'] = self.cs.co.create(db, actor.id, rid)
            record['status'] = 'ASSESSING'
            record['payload'].update(needs=None, note='Interpreting this service request. No advice, review or action is authorised.',
                naturalIntent={'version': 1, 'operationId': new_id('CSI'), 'message': message,
                               'stage': 'INTERPRETING', 'simulated': mode})
            Store.save(db, record)
            try:
                record['payload']['policy'] = self.policy(db, record)
            except DomainError as error:
                return self.blocked_policy(db, record, error)
            Store.save(db, record)
            self.cs.co.state(db, record['payload']['coordinationId'], 'PENDING_VALIDATION',
                             'INTENT_CONTEXT_SAVED', {'contextRevision': record['revision']})
            self.cs.co.supersede_pending(db, record['payload']['coordinationId'], record['revision'])
            Store.event(db, rid, 'CS', 'INTENT_STARTED', {'contextRevision': record['revision'], 'simulated': mode})
            scope = deepcopy(record)
        # No DB connection/transaction is open during shared model inference.
        outcome = None
        try:
            receiver = getattr(self.llm, 'interpret_service_request', None)
            if not callable(receiver):
                raise ModelError('CS intent capability is unavailable; no substitute was used.', 503, 'LLM_CAPABILITY_UNAVAILABLE')
            outcome = validate_intent(receiver(message), message)
            error_code = None
        except (ValueError, TypeError, KeyError):
            error_code = 'LLM_INVALID_OUTPUT'
        except ModelError as error:
            error_code = error.code if error.code in {'LLM_UNAVAILABLE','LLM_TIMEOUT','LLM_HTTP','LLM_INVALID_OUTPUT','LLM_CAPABILITY_UNAVAILABLE'} else 'LLM_INVALID_OUTPUT'
        except Exception:
            error_code = 'LLM_UNAVAILABLE'
        with self.store.transaction() as db:
            self.identity(db, actor, 'CUSTOMER', authenticate)
            record = self.cs.owned(db, actor, rid)
            current = record['payload'].get('naturalIntent', {})
            if (record['revision'] != scope['revision'] or record['owner_id'] != scope['owner_id']
                    or record['payload']['orderId'] != scope['payload']['orderId']
                    or record['payload'].get('policy') != scope['payload'].get('policy')
                    or record['payload']['coordinationId'] != scope['payload']['coordinationId']
                    or current != scope['payload']['naturalIntent'] or record['status'] != 'ASSESSING'):
                raise DomainError('An old intent response was discarded. Use the current request.', 409, 'STALE_SCOPE')
            try:
                self.policy(db, record)
            except DomainError as error:
                return self.blocked_policy(db, record, error)
            if error_code:
                current.update(stage='FAILED', errorCode=error_code)
                record['status'] = 'UNRESOLVED'
                note = 'Service intent could not be completed (' + error_code + '). Correct the request or seek Founder assistance; no mock fallback or action occurred.'
            else:
                current['interpretation'] = outcome
                missing = [key for key in ('concern','budget','fragranceFree') if outcome['needs'][key] is None]
                if outcome['intent'] == 'UNSUPPORTED':
                    current['stage'] = 'UNSUPPORTED'; record['status'] = 'UNRESOLVED'
                    note = 'This bounded scene supports exchanges only. Request Founder assistance; no refund, cancellation or other action was inferred.'
                elif outcome['intent'] != 'EXCHANGE' or missing:
                    current['stage'] = 'CLARIFICATION_REQUIRED'; record['status'] = 'NEEDS_INFORMATION'
                    current['questions'] = (['Explicitly request an exchange, or seek Founder assistance.'] if outcome['intent'] != 'EXCHANGE' else []) + [
                        {'concern':'State hydration/dry-skin or cleansing need.', 'budget':'State an explicit AUD budget.',
                         'fragranceFree':'State whether fragrance-free is required or optional.'}[key] for key in missing]
                    note = 'Clarification required. ' + ' '.join(current['questions'])
                else:
                    current['stage'] = 'READY'
                    record['payload']['needs'] = validated_needs({'message':message, **{key:outcome['needs'][key] for key in ('concern','budget','fragranceFree')}})
                    note = 'Interpreted exchange needs are shown for review. Founder must initiate advice; Customer confirmation and exact approval remain required.'
            record['payload']['note'] = note
            Store.save(db, record)
            self.cs.co.state(db, record['payload']['coordinationId'],
                'PENDING_VALIDATION' if current['stage']=='READY' else 'CLARIFICATION_REQUIRED' if record['status']=='NEEDS_INFORMATION' else 'ESCALATED',
                'INTENT_RECORDED', {'contextRevision': record['revision'], 'stage': current['stage'], 'businessExecution':False})
            Store.event(db, rid, 'CS', 'INTENT_RECORDED', {'contextRevision':record['revision'], 'stage':current['stage'], 'simulated':mode})
            return record

    @storage_boundary
    def coordinate(self, actor, rid, data, authenticate=None):
        require_role(actor, 'FOUNDER')
        if set(data) - {'contextRevision'}:
            raise DomainError('Handoff accepts only the current contextRevision.')
        live = not self.cs.advisor.simulated
        revision = revision_value(data.get('contextRevision')) if live or data else None
        with self.store.transaction() as db:
            self.identity(db, actor, 'FOUNDER', authenticate)
            record = Store.get(db, rid, 'CS')
            if revision is not None and revision != record['revision']:
                raise DomainError('The request changed. Start the current handoff.', 409, 'STALE_SCOPE')
            if record['status'] != 'ASSESSING':return record
            intent = record['payload'].get('naturalIntent')
            if (live and not intent) or (intent and intent.get('stage') != 'READY'):
                raise DomainError('A current completed service interpretation is required. Correct the natural service request first.', 409, 'CS_INTENT_REQUIRED')
            if not live:
                return self.cs.coordinate(db, actor, rid)
            try:
                self.policy(db, record)
            except DomainError as error:
                return self.blocked_policy(db, record, error)
            handoff = self.cs.co.prepare_external(db, record['payload']['coordinationId'], record['payload']['needs'], False)
            if handoff is None:return record
            record['payload']['note'] = 'Read-only advice handoff is in progress. No confirmation, approval or exchange has completed.'
            Store.save(db, record)
            scope = deepcopy(record); products = catalogue(db)
        try:
            advice = self.cs.advisor.recommend_from_catalogue(scope['payload']['needs'], products)
        except Exception:
            advice = {'status':'INCOMPLETE','simulated':False,'errorCode':'LLM_UNAVAILABLE',
                      'message':'The read-only advice service failed. No substitute was used.'}
        with self.store.transaction() as db:
            self.identity(db, actor, 'FOUNDER', authenticate)
            current = Store.get(db, rid, 'CS')
            if (current['owner_id'] != scope['owner_id'] or current['revision'] != scope['revision']
                    or current['payload'] != scope['payload'] or current['status'] != 'ASSESSING'):
                raise DomainError('An old advice response was discarded. Use the current request.', 409, 'STALE_SCOPE')
            try:
                self.policy(db, current)
            except DomainError as error:
                return self.blocked_policy(db, current, error)
            result = self.cs.co.finish_external(db, current['payload']['coordinationId'], handoff['handoffId'], advice)
            return self.cs._receive_advice(db, current, result)
