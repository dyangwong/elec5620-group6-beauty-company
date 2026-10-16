"""Run from the repository root: python3 -m beauty_company."""
import argparse
import os
from pathlib import Path

from .application import Company
from .http import make_server


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="ELEC5620 local simulation workspace")
    parser.add_argument("--port", type=int, default=int(os.environ.get("BEAUTY_PORT", "5620")))
    parser.add_argument("--db", default=os.environ.get("BEAUTY_DB", str(root / "var/company.sqlite3")))
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Choose a port between 1 and 65535.")
    server = make_server(Company(args.db), args.port)
    print(f"Beauty Company · local simulation\nLocal: http://127.0.0.1:{args.port}\nAll model, media and commerce capabilities are simulated.\nPress Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
