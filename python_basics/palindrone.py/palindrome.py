def is_palindrome(text: str) -> bool:
    """Return True when the provided string reads the same forward and backward."""
    return text == text[::-1]