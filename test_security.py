from html import escape

from security import create_profile_html

# prompt to AI generate tests for this function, making sure to tests the security aspect as well (i.e HTML injection)
def test_create_profile_html_renders_values() -> None:
    html = create_profile_html("Alice", 30, "NYC")

    assert "<h1>Alice</h1>" in html
    assert "<p>Age: 30</p>" in html
    assert "<p>Location: NYC</p>" in html


def test_create_profile_html_escapes_html_injection() -> None:
    malicious_name = "<script>alert('x')</script>"
    malicious_location = "<b>NY</b>"

    html = create_profile_html(malicious_name, 25, malicious_location)

    assert "<script>alert('x')</script>" not in html
    assert "<b>NY</b>" not in html
    assert escape(malicious_name) in html
    assert escape(malicious_location) in html
    assert "<h1>" in html
    assert "</h1>" in html
