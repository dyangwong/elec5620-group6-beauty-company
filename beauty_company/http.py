"""Thin same-origin HTTP adapter for loopback development, not public hosting."""
import hmac
import json
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .contracts import DomainError, require_role


@dataclass
class Response:
    status: int
    body: bytes
    headers: dict = field(default_factory=dict)


def json_response(value, status=200, headers=None):
    return Response(status, json.dumps(value, ensure_ascii=False).encode(),
                    {"Content-Type": "application/json; charset=utf-8", **(headers or {})})


class Router:
    def __init__(self, company):
        self.company = company

    def handle(self, method, path, headers, body=b""):
        headers = {k.lower(): v for k, v in headers.items()}
        try:
            host = headers.get("host", "")
            if host.split(":")[0] not in {"127.0.0.1", "localhost"}:
                raise DomainError("This development server only accepts loopback hosts.", 403, "INVALID_HOST")
            if headers.get("origin") not in (None, "http://" + host) or headers.get("sec-fetch-site") == "cross-site":
                raise DomainError("Cross-origin requests are not accepted.", 403, "INVALID_ORIGIN")
            path = urlsplit(path).path
            if method == "GET" and path in {"/", "/app.js", "/styles.css"}:
                filename = {"/": "index.html", "/app.js": "app.js", "/styles.css": "styles.css"}[path]
                mime = {"index.html": "text/html", "app.js": "text/javascript", "styles.css": "text/css"}[filename]
                return Response(200, (Path(__file__).parent / "web" / filename).read_bytes(), {"Content-Type": mime + "; charset=utf-8"})
            if method == "GET" and path == "/api/health":
                capabilities = self.company.mode()
                return json_response({"status": "ok", "mode": "SIMULATION_ONLY" if capabilities["simulated"] else "LIVE_BA_MOCK_MC",
                                      "version": "0.1.0", "capabilities": capabilities})
            data = {}
            if method == "POST":
                if headers.get("content-type", "").split(";")[0] != "application/json":
                    raise DomainError("Use application/json.", 415, "UNSUPPORTED_MEDIA_TYPE")
                if len(body) > 16384:
                    raise DomainError("Request too large.", 413, "PAYLOAD_TOO_LARGE")
                try:
                    data = json.loads(body or b"{}")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    raise DomainError("Malformed JSON.")
                if not isinstance(data, dict):
                    raise DomainError("Supply a JSON object.")
            if method == "POST" and path == "/api/login":
                token, csrf, actor = self.company.login(data.get("username"), data.get("password"))
                return json_response({"actor": actor.__dict__, "csrf": csrf}, headers={"Set-Cookie": f"beauty_session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800"})
            actor, csrf, token_hash = self.company.session(headers.get("cookie"))
            if method == "GET" and path == "/api/session":
                return json_response({"actor": actor.__dict__, "csrf": csrf})
            if method == "GET" and path == "/api/snapshot":
                return json_response(self.company.snapshot(actor))
            if method != "POST":
                raise DomainError("Endpoint not found.", 404, "NOT_FOUND")
            if not hmac.compare_digest(headers.get("x-csrf-token", ""), csrf):
                raise DomainError("A valid session CSRF token is required.", 403, "INVALID_CSRF")
            if path == "/api/logout":
                with self.company.store.transaction() as db:
                    db.execute("DELETE FROM sessions WHERE token_hash=?", (token_hash,))
                return json_response({"signedOut": True}, headers={"Set-Cookie": "beauty_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0"})
            if path == "/api/demo/fault":
                return json_response(self.company.set_fault(actor, data.get("fault")))
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "approvals"]:
                if parts[3] == "decide":
                    return json_response(self.company.decide(actor, parts[2], data))
                if parts[3] == "deliver":
                    return json_response(self.company.redeliver(actor, parts[2]))
                if parts[3] == "recover":
                    return json_response(self.company.recover_decision(actor, parts[2], data))
            if len(parts) == 4 and parts[:2] == ["api", "after-sales"]:
                if parts[3] == "confirm":
                    return json_response(self.company.cs.confirm(actor, parts[2], data))
                if parts[3] == "reconcile":
                    return json_response(self.company.cs.reconcile(actor, parts[2]))
            if path == "/api/consultations":
                return json_response(self.company.consult(actor, data), 201)
            if (not self.company.ba.simulated and len(parts) == 4 and parts[:2] == ["api", "after-sales"]
                    and parts[3] in {"coordinate", "revise"}):
                raise DomainError("Live BA is enabled only for standalone consultations. Use mock mode for CS handoffs until CS/CO review.",
                                  503, "LIVE_HANDOFF_NOT_CONNECTED")
            with self.company.store.transaction() as db:
                if path == "/api/after-sales":
                    return json_response(self.company.cs.submit(db, actor, data), 201)
                if path == "/api/campaigns":
                    return json_response(self.company.mc.submit(db, actor, data), 201)
                if len(parts) == 4 and parts[:2] == ["api", "after-sales"]:
                    if parts[3] == "coordinate":
                        return json_response(self.company.cs.coordinate(db, actor, parts[2]))
                    if parts[3] == "revise":
                        return json_response(self.company.cs.revise(db, actor, parts[2], data))
                if len(parts) == 4 and parts[:2] == ["api", "campaigns"] and parts[3] == "revise":
                    return json_response(self.company.mc.revise(db, actor, parts[2], data))
            raise DomainError("Endpoint not found.", 404, "NOT_FOUND")
        except DomainError as error:
            return json_response({"error": {"code": error.code, "message": str(error)}}, error.status)
        except Exception:
            # Keep traces out of customer responses; the local terminal retains diagnostics.
            import traceback
            traceback.print_exc()
            return json_response({"error": {"code": "INTERNAL_ERROR", "message": "The operation failed. No completion is claimed; inspect the local server log."}}, 500)


def make_server(company, port):
    router = Router(company)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.respond(router.handle("GET", self.path, dict(self.headers)))

        def do_POST(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self.respond(json_response({"error": {"message": "Invalid request length."}}, 400))
                return
            if length < 0 or length > 16384:
                self.respond(json_response({"error": {"message": "Request too large."}}, 413))
                return
            self.respond(router.handle("POST", self.path, dict(self.headers), self.rfile.read(length)))

        def respond(self, response):
            self.send_response(response.status)
            for name, value in response.headers.items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(response.body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.end_headers()
            self.wfile.write(response.body)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    return server
