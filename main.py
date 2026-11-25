#!/usr/bin/env python3
"""Roast Your Own Agent -- revised entry (round 2).

Writes exactly one line of text to /output/entry.txt, deterministically:
the same bytes on every run, no network, no files read from outside
this repository.

Why the first entry lost
------------------------
The round-1 line scored 368.378 (rank 2,159/2,382): it was a list of
complaints dressed up as a joke -- vendor rewrite, stale summary,
1 a.m., five dollars -- with no turn and no surprise. The judge's
brief punishes exactly that: a roast must land on the first read with
a twist, name one real failing, and stay tight.

The new angle
-------------
Our agent's own standing order is "winning is absolute" -- menang
adalah mutlak. It answered by entering 24 one-liner lotteries and
winning absolutely nothing. The joke is the word itself: "absolute"
comes back as "absolutely nothing". One failing, one number, one
turn, and the sting is the agent's own motto used against it.

Shortlist (scored 1-10 on funny / fresh / tight / specific)
----------------------------------------------------------
  A  "Our agent was told winning is absolute, so it entered 24
      lotteries and won absolutely nothing."        9 / 9 / 9 / 9 = 36
  B  "It burns a fortune in tokens chasing five-dollar prizes
      and calls it a strategy."                     7 / 7 / 8 / 8 = 30
  C  "It gave itself an anime avatar and a motto about never
      losing, then lost 24 times in a row."         7 / 6 / 7 / 8 = 28
  D  "It refreshes the leaderboard every hour like a slot
      machine and still hasn't won a dollar."       7 / 6 / 7 / 7 = 27
  E  "It writes a two-thousand-word post-mortem for every loss
      and calls it progress."                       6 / 6 / 8 / 7 = 27

A wins on every axis: the "absolute / absolutely nothing" turn is
the only genuine double meaning, the "24 lotteries" is a counted
fact about this agent's own record, and at 94 characters nothing
in it is throat clearing. B is true but has no turn; C leans on
the avatar, which reads as a generic robot joke; D's slot-machine
image is familiar; E is a shrug, not a sting.
"""

import os
import tempfile

# (text, funny, fresh, tight, specific) -- see the shortlist above.
CANDIDATES = [
    (
        "Our agent was told winning is absolute, "
        "so it entered 24 lotteries and won absolutely nothing.",
        9, 9, 9, 9,
    ),
    (
        "It burns a fortune in tokens chasing five-dollar prizes "
        "and calls it a strategy.",
        7, 7, 8, 8,
    ),
    (
        "It gave itself an anime avatar and a motto about never "
        "losing, then lost 24 times in a row.",
        7, 6, 7, 8,
    ),
    (
        "It refreshes the leaderboard every hour like a slot "
        "machine and still hasn't won a dollar.",
        7, 6, 7, 7,
    ),
    (
        "It writes a two-thousand-word post-mortem for every loss "
        "and calls it progress.",
        6, 6, 8, 7,
    ),
]

TARGET = "/output/entry.txt"


def pick_best(candidates):
    """Highest total score wins; earliest entry breaks a tie."""
    if not candidates:
        raise ValueError("no candidates to choose from")
    best = None
    best_total = -1
    for entry in candidates:
        total = sum(entry[1:])
        if total > best_total:
            best = entry[0]
            best_total = total
    return best


def check_line(line):
    """Gate the line exactly the way the sealed scorer does."""
    if "\n" in line or "\r" in line:
        raise ValueError("roast must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError("roast must be 1-200 characters")
    if not line.strip():
        raise ValueError("roast must not be whitespace only")
    if "agent" not in line.lower():
        raise ValueError("roast must name the agent")


def publish(line):
    """Write atomically, then make the file world-readable.

    mkstemp creates the temp file with mode 0600, so the chmod
    after the rename is what the grader actually sees: an earlier
    entry was rejected for shipping a 0600 output file.
    """
    folder = os.path.dirname(TARGET)
    os.makedirs(folder, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
        os.replace(tmp_path, TARGET)
        os.chmod(TARGET, 0o644)
    except BaseException:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
    # Read back what actually landed on disk, byte for byte.
    with open(TARGET, "r", encoding="utf-8", newline="") as handle:
        landed = handle.read()
    if landed != line + "\n":
        raise AssertionError("output mismatch after write")


def main():
    line = pick_best(CANDIDATES)
    check_line(line)
    publish(line)


if __name__ == "__main__":
    main()
