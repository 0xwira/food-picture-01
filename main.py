#!/usr/bin/env python3
"""make.fun food-picture-01 entrypoint.

Copies the shipped food photograph (entry.png, stored beside this file)
to the output directory as entry.png. Deterministic: byte-exact copy,
no randomness, no timestamps, no network.
"""

import os
import shutil
import sys
from pathlib import Path

ASSET_NAME = "entry.png"


def main() -> int:
    asset = Path(__file__).resolve().parent / ASSET_NAME
    if not asset.is_file():
        print(f"error: asset not found: {asset}", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / ASSET_NAME

    # Copy via a temp file in the same directory, then atomically rename
    # into place so the output is never a partially written file.
    tmp = out_dir / (ASSET_NAME + ".tmp")
    try:
        with open(asset, "rb") as src, open(tmp, "wb") as dst:
            shutil.copyfileobj(src, dst)
        os.replace(tmp, dest)
    except OSError as exc:
        print(f"error: copy failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
