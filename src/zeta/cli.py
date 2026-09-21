from __future__ import annotations

import argparse
import os

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Zeta AI chat app")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")))
    parser.add_argument(
        "--reload",
        action="store_true",
        default=os.getenv("UVICORN_RELOAD", "0") == "1",
    )
    args = parser.parse_args()
    uvicorn.run("zeta.app:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
