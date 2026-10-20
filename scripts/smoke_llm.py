"""Real HTTP BA probe; no provider fakes. Failure exits nonzero and is retained locally."""
import argparse
import json
import time
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.request import HTTPCookieProcessor, ProxyHandler, Request, build_opener


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=5620)
    parser.add_argument("--expect-mode", choices=("mock", "strata"), default="strata")
    parser.add_argument("--output-dir", default="var/verification")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Invalid local port")
    opener = build_opener(ProxyHandler({}), HTTPCookieProcessor(CookieJar()))
    base = f"http://127.0.0.1:{args.port}"
    report = {"dateUtc": datetime.now(timezone.utc).isoformat(), "expectedMode": args.expect_mode,
              "transport": "actual local HTTP", "passed": False}
    started = time.monotonic()

    def call(path, data=None, csrf=None):
        headers = {"Content-Type": "application/json"}
        if csrf:
            headers["X-CSRF-Token"] = csrf
        request = Request(base + path, None if data is None else json.dumps(data).encode(), headers)
        with opener.open(request, timeout=310) as response:
            return json.load(response)

    try:
        health = call("/api/health")
        report["capabilities"] = health["capabilities"]
        expected = "LIVE" if args.expect_mode == "strata" else "MOCK"
        if health["capabilities"]["ba"] != expected:
            raise ValueError("The app is not configured in the requested BA mode.")
        login = call("/api/login", {"username": "customer", "password": "customer-demo"})
        result = call("/api/consultations", {"message": "I would like a fragrance-free moisturiser for dry skin.",
                      "concern": "HYDRATION", "budget": 60, "fragranceFree": True}, login["csrf"])
        report["record"] = result
        advice = result["payload"].get("result", {})
        report["passed"] = (result["status"] == "COMPLETED" and advice.get("simulated") is (expected == "MOCK")
                            and advice.get("product", {}).get("id") == "P-101"
                            and bool(advice.get("reasons"))
                            and all(f in advice["product"]["facts"] for f in advice["reasons"]))
    except Exception as error:
        # Do not print HTTP response bodies, headers, cookies or local config contents.
        report["errorType"] = type(error).__name__
    report["elapsedSeconds"] = round(time.monotonic() - started, 3)
    folder = Path(args.output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = folder / f"ba-{args.expect_mode}-{stamp}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"BA {args.expect_mode}: {'PASS' if report['passed'] else 'FAIL'}; evidence: {path}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
