import time

import pytest

from performance import has_duplicates

# used the prompt to the AI "test the performance of the has_duplicates function"

def test_has_duplicates_basic_cases() -> None:
    assert has_duplicates([1, 2, 3, 1]) is True
    assert has_duplicates([1, 2, 3, 4]) is False


def test_has_duplicates_large_non_duplicate_list_performance() -> None:
    items = list(range(2500))
    start = time.perf_counter()
    result = has_duplicates(items)
    elapsed = time.perf_counter() - start

    assert result is False
    assert elapsed < 2.0, f"Expected performance under 2 seconds, got {elapsed:.3f}s"


def test_has_duplicates_large_duplicate_list_performance() -> None:
    items = list(range(2500))
    items.append(items[0])
    start = time.perf_counter()
    result = has_duplicates(items)
    elapsed = time.perf_counter() - start

    assert result is True
    assert elapsed < 2.0, f"Expected performance under 2 seconds, got {elapsed:.3f}s"
