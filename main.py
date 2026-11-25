#!/usr/bin/env python3
"""The Battery's Last Text to Its Charger — entry program.

The entry is a single fixed line: a dying phone battery's breakup text
to the charger that spent the day charging someone else's phone. This
program checks the line against the bounty gate (the kit's RULES.txt:
UTF-8 text of 1 to 200 characters, not only white space, one line),
writes it to entry.txt with no trailing newline, then reads the file
back and compares it byte for byte so a silent truncation or encoding
slip fails loudly instead of shipping. The string never changes, so
every run writes identical bytes. Standard library only; no network,
no randomness, no clock.
"""

import os
import sys

TEXT = "I saw you charging your ex's phone last night. Don't text back. I'm at 1% and I'd rather die than share a cable."

LOW = 1
HIGH = 200


def gate_errors(text):
    """List the ways `text` breaks the bounty gate; empty means it passes."""
    errors = []
    if len(text) < LOW or len(text) > HIGH:
        errors.append(
            "entry is %d characters, gate allows %d-%d" % (len(text), LOW, HIGH)
        )
    if text.strip() == "":
        errors.append("entry is only white space")
    if any(mark in text for mark in ("\r", "\n")):
        errors.append("entry must be a single line, no line breaks")
    return errors


def main():
    errors = gate_errors(TEXT)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")

    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(TEXT)

    with open(target, "rb") as handle:
        raw = handle.read()
    if raw.decode("utf-8") != TEXT:
        print("entry.txt came back different from the entry", file=sys.stderr)
        return 1
    if len(raw) != len(TEXT.encode("utf-8")):
        # Same text but different bytes would mean an encoding slip:
        # the judge reads the file's bytes, so the bytes must match too.
        print("entry.txt byte length does not match the entry", file=sys.stderr)
        return 1

    print("entry.txt written: %d characters" % len(TEXT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
