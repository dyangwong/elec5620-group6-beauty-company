"""KAN-15 CS intent v1: hypotheses only; no identity, policy or action authority."""
import re
from .needs import mock_extract, validate_extraction

EXCHANGE = r'\bexchange\b|\bswap\b|\breplace(?:ment)?\b|换货|更换'
UNSUPPORTED = r'\brefund\b|\breturn\b|\bcancel\b|退款|退货|取消|诊断|治疗|diagnos|treat eczema'
NEGATED = r"\b(?:do not|don't|not|never)\b.{0,35}(?:exchange|swap|replace)|(?:不想|不要|不需要).{0,12}(?:换货|更换)"


def validate_intent(value, message):
    if (not isinstance(value, dict) or set(value) != {'intent', 'intentSource', 'needs'}
            or value['intent'] not in ('EXCHANGE', 'CLARIFY', 'UNSUPPORTED')):
        raise ValueError('Invalid CS intent schema')
    source = value['intentSource']
    if source is not None and (not isinstance(source, str) or not source.strip()
                               or len(source) > 600 or source not in message):
        raise ValueError('Intent source must be a literal Customer quotation')
    needs = validate_extraction(value['needs'], [message])
    # Bounded lexical corroboration complements quoted model hypotheses; unknown wording clarifies.
    concern = needs['concern']
    patterns = {'HYDRATION':r'hydrat\w*|dry skin|moisturi\w*|保湿|干燥|干皮',
                'CLEANSING':r'cleans\w*|face wash|洁面|清洁'}
    if concern is not None and not re.search(patterns[concern], needs['sources']['concern'], re.I):
        raise ValueError('Product need is unsupported by its quotation')
    observed = mock_extract([message])
    # Mixed product needs/multiple explicit budgets cannot be resolved by guessing.
    if all(re.search(pattern, message, re.I) for pattern in patterns.values()):
        needs['concern'] = needs['sources']['concern'] = None
    if needs['budget'] is not None and observed['budget'] is None:
        needs['budget'] = needs['sources']['budget'] = None
    fragrance = needs['fragranceFree']
    if fragrance is not None:
        fragrance_source = needs['sources']['fragranceFree']
        corroborated = mock_extract([fragrance_source])['fragranceFree']
        if corroborated is None or corroborated != fragrance:
            raise ValueError('Fragrance constraint cannot be silently relaxed')
    intent = value['intent']
    if intent == 'EXCHANGE' and (source is None or not re.search(EXCHANGE, source, re.I)):
        raise ValueError('Exchange intent needs explicit exchange wording')
    # Conservative boundary: mixed/negated/unsupported requests never become authority.
    if re.search(UNSUPPORTED, message, re.I):
        intent = 'UNSUPPORTED'
    elif re.search(NEGATED, message, re.I):
        intent = 'CLARIFY'
    return {'intent': intent, 'intentSource': source, 'needs': needs}


def mock_intent(message):
    match = re.search(EXCHANGE, message, re.I)
    return validate_intent({'intent': 'EXCHANGE' if match else 'CLARIFY',
                            'intentSource': match[0] if match else None,
                            'needs': mock_extract([message])}, message)
