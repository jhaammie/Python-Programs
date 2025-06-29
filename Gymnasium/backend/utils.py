import re

def slugify(text):
    """Convert a string to a slug format, handling Swedish characters."""
    # Convert to lowercase
    text = text.lower()
    # Replace Swedish characters with their ASCII equivalents
    text = text.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
    # Replace non-alphanumeric characters with a hyphen
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading and trailing hyphens
    text = text.strip('-')
    return text 
