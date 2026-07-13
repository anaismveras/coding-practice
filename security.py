from html import escape

# prompt AI "suggest security improvements for this function"

def create_profile_html(name: str, age: int, location: str) -> str:
    safe_name = escape(name)
    safe_location = escape(location)

    return f"""
    <html>
        <head><title>{safe_name}'s Profile</title></head>
        <body>
            <h1>{safe_name}</h1>
            <p>Age: {age}</p>
            <p>Location: {safe_location}</p>
        </body>
    </html>
    """
