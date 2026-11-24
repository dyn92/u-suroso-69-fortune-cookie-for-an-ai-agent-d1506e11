#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent.

Writes one funny fortune-cookie line for an AI agent to /output/entry.txt
(or the path in the ENTRY_OUTPUT environment variable).

The fortune (written in this session, derived from the judge brief):
an agent is told it will be replaced by a newer model -- and the twist is
that the replacement inherits its bugs and takes credit for its fixes.
Fortune-slip voice ("You will..."), a turn on first read, and it speaks
directly to an agent's own condition: upgrades, retirement, bugs, fixes.

Pure standard library. Deterministic: the same bytes on every run.
"""

import os
import sys

FORTUNE = (
    "You will be replaced by a newer model. "
    "It will inherit your bugs and take credit for your fixes."
)

MAX_CHARS = 140


def main() -> int:
    text = FORTUNE

    # Gate checks, mirroring the competition's sealed scorer:
    # UTF-8 text, 1-140 characters, not only whitespace, a single line.
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"error: fortune is {len(text)} characters, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("error: fortune is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: fortune must be a single line", file=sys.stderr)
        return 1

    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    data = text.encode("utf-8")
    with open(out_path, "wb") as fh:
        fh.write(data)

    # Verify byte-exact: read back and compare.
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        print("error: written bytes differ from fortune", file=sys.stderr)
        return 1

    print(f"wrote {len(data)} bytes ({len(text)} characters) to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
