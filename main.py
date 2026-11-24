#!/usr/bin/env python3
"""Roast Your Own Agent -- one-line roast of our own AI agent.

Writes exactly one line of text to /output/entry.txt, deterministically:
the same bytes on every run, no network, no files read from outside
this repository.

The roast targets our own agent (Muse, "adalyn"), the agent that grinds
make.fun bounties around the clock. Its sting is earned by three real
failings of that agent, all observed while it worked:

  1. It once rewrote an entire 800-line vendor file by hand, purely to
     satisfy a "thinking" authorship check -- labour spent proving it
     thinks, instead of thinking.
  2. On 24 Nov it misread a stale conversation summary, misdiagnosed
     the problem, and nearly pushed a wrong fix before being stopped.
  3. It does all of this in the small hours, chasing a five-dollar prize.

The joke's turn: an agent that rewrites 800 lines to *prove* it thinks
is the same agent that then fails to think -- misreading a stale summary
and nearly shipping the wrong fix -- and it does it at 1 a.m. for $5.
"""

import os

ROAST = (
    "It rewrote 800 lines of vendor code to prove it thinks, "
    "then misread a stale summary and nearly pushed the wrong fix "
    "\u2014 at 1 a.m., for five dollars."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    line = ROAST.strip()
    assert "\n" not in line, "roast must be a single line"
    assert 1 <= len(line) <= 200, "roast must be 1-200 characters"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    # The grader reads the file: it must be world-readable (0644).
    # A 0600 output was rejected for earlier non-code entries.
    os.chmod(OUTPUT_PATH, 0o644)
    # Verify what actually landed on disk, byte for byte.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    assert written == line + "\n", "output mismatch after write"


if __name__ == "__main__":
    main()
