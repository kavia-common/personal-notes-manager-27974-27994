#!/usr/bin/env python3
"""
PUBLIC_INTERFACE
Helper script to regenerate the OpenAPI schema file for the Notes backend.

Usage:
    python scripts/generate_openapi.py --base-url http://localhost:3001 --out ../interfaces/openapi.json

Notes:
- Requires the backend to be running and serving /openapi.json (FastAPI default).
- This script intentionally avoids hardcoding URLs and paths; provide them via CLI args or env.
"""
import argparse
import os
import sys
import json
from urllib.request import urlopen

# PUBLIC_INTERFACE
def main():
    """Fetches /openapi.json from a running backend and writes it to the specified output file."""
    parser = argparse.ArgumentParser(description="Regenerate OpenAPI schema from running backend")
    parser.add_argument("--base-url", default=os.getenv("NOTES_API_BASE_URL", "http://localhost:3001"),
                        help="Base URL of the running backend (default: http://localhost:3001 or NOTES_API_BASE_URL)")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "interfaces", "openapi.json"),
                        help="Output path for the OpenAPI JSON file")
    args = parser.parse_args()

    openapi_url = args.base_url.rstrip("/") + "/openapi.json"
    try:
        with urlopen(openapi_url) as resp:
            data = resp.read()
            spec = json.loads(data.decode("utf-8"))
    except Exception as e:
        print(f"Failed to fetch OpenAPI from {openapi_url}: {e}", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote OpenAPI schema to {out_path}")

if __name__ == "__main__":
    main()
