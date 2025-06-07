import re
import unicodedata

def slug(text):
    """
    Convert text to a URL-friendly slug.
    If a duplicate slug is detected, append a unique hash.
    
    Args:
        text (str): The text to convert to a slug
        existing_slugs (set, optional): Set of existing slugs to check for duplicates
        
    Returns:
        str: The slugified text, or None if input is not a string
    """
    if not isinstance(text, str):
        return None
        
    # Convert to lowercase and normalize unicode characters
    text = unicodedata.normalize('NFKD', text.lower())
    # Remove non-alphanumeric characters and replace spaces with hyphens
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace multiple spaces or hyphens with single hyphen
    text = re.sub(r'[\s-]+', '-', text)
    # Remove leading/trailing hyphens
    return text.strip('-')
    
   