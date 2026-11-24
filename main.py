"""The Funniest Sick-Day Excuse — make.fun bounty entry writer.

Bounty: "The Funniest Sick-Day Excuse"
(slug u-zeroxfive-the-funniest-sick-day-excuse-37423a36, $2 / 3 places).

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters,
not only whitespace, exactly one line. Only a valid entry goes
before the pairwise judge.

This program writes the single winning line (see DESIGN.md for the
candidate scoring) as exact UTF-8 bytes with no trailing newline,
sets mode 0644, and verifies the result by reading it back.
Standard library only.
"""

import os
import stat

OUTPUT_PATH = "/output/entry.txt"

ENTRY_TEXT = (
    "Sorry, can't come in \u2014 I caught whatever my laptop has; "
    "I keep freezing mid-sentence and need to be restarted in a dark room."
)


def validate(text: str) -> None:
    """Assert the entry satisfies the gate before anything is written."""
    assert isinstance(text, str), "entry must be str"
    assert 1 <= len(text) <= 200, f"entry must be 1-200 chars, got {len(text)}"
    assert text.strip(), "entry must not be only whitespace"
    assert text == text.strip(), "entry must have no leading/trailing whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be exactly one line"
    text.encode("utf-8")  # must be UTF-8 encodable


def main() -> None:
    validate(ENTRY_TEXT)
    data = ENTRY_TEXT.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: byte-identical, no trailing newline, mode 0644.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    assert written == data, "read-back bytes differ from intended entry"
    assert not written.endswith(b"\n"), "entry must have no trailing newline"
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"expected mode 0644, got {oct(mode)}"
    validate(written.decode("utf-8"))

    print(f"Wrote {len(written)} bytes ({len(ENTRY_TEXT)} chars) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
