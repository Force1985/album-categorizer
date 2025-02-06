"""
Info notes transformations
"""
import re

def remove_bbcode_urls(text: str) -> str:
    """
    Remove BBCode URL tags from text and keep only the link text.
    
    Args:
        text: Text containing BBCode URL tags
        
    Returns:
        Text with URL tags removed, keeping only the link text
    """
    if not text:
        return ''
    
    # Pattern to match BBCode URL tags: [url=...]text[/url]
    pattern = r'\[url=.*?\](.*?)\[/url\]'
    return re.sub(pattern, r'\1', text)

def transform_info_notes(notes: str, artist: str, format_descriptions: list[str]) -> str:
    """
    Transform notes text based on format descriptions
    
    Args:
        notes: Original notes text from API
        artist: Artist name
        format_descriptions: List of format descriptions from API
        
    Returns:
        Transformed notes with artist credit line and URLs removed
    """
    if not artist:
        return remove_bbcode_urls(notes) if notes else ''
        
    # Check if 'Mixed' is in format descriptions
    is_mixed = any(desc.lower() == 'mixed' for desc in format_descriptions)
    
    # Create credit line based on format
    credit_line = f"Mixed by {artist}." if is_mixed else f"Written & produced by {artist}."
    
    # Combine credit line with original notes, removing URLs from notes
    if notes:
        cleaned_notes = remove_bbcode_urls(notes)
        return f"{credit_line}\n{cleaned_notes}"
    return credit_line
