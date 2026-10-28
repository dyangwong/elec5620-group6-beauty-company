"""Run from the repository root: python3 -m beauty_company."""
import argparse
import os
from pathlib import Path

from .application import Company
from .http import make_server
from .adapters.llm import create_llm


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="ELEC5620 local simulation workspace")
    parser.add_argument("--port", type=int, default=int(os.environ.get("BEAUTY_PORT", "5620")))
    parser.add_argument("--db", default=os.environ.get("BEAUTY_DB", str(root / "var/company.sqlite3")))
    parser.add_argument("--llm-mode", choices=("mock", "strata"), default="mock")
    parser.add_argument("--llm-config", help="Local JSON configuration; required for Strata live text")
    parser.add_argument("--mc-live", action="store_true", help="Opt in to bounded live MC text; Strata required, media stays mock")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Choose a port between 1 and 65535.")
    try:
        company = Company(args.db, llm=create_llm(args.llm_mode, args.llm_config, mc_live=args.mc_live))
    except (ValueError, OSError, TypeError) as error:
        parser.error(str(error))
    server = make_server(company, args.port)
    print(f"Beauty Company\nLocal: http://127.0.0.1:{args.port}\nBA: {company.mode()['ba']}; MC text: {company.mode()['mc']}; media and commerce: simulated.\nConfigured live mode is not a model health check.\nPress Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
