from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent))

from palindrome import is_palindrome


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("racecar", True),
        ("level", True),
        ("hello", False),
        ("", True),
    ],
)
def test_is_palindrome_returns_expected_result(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected


def test_is_palindrome_handles_simple_palindrome_without_spaces() -> None:
    assert is_palindrome("level") is True
