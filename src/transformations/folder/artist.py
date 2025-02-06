"""
Artist name transformations
"""
import re

def transform_artist(artist: str, format_descriptions: list[str]) -> str:
    """
    Transform a single artist name
    
    Args:
        artist: Artist name string
        
    Returns:
        Transformed artist name
    """
    if not artist:
        return artist
        
    # Check if 'Mixed' is in format descriptions
    is_mixed = any(desc.lower() == 'mixed' for desc in format_descriptions)

    # Return 'VA' if 'Mixed' is present
    if is_mixed:
        return 'VA'

    # Check for Various Artists variations
    if artist.lower() in ['various', 'various artists', 'v/a', 'va']:
        return 'VA'
    
    # Remove numbers in parentheses (e.g., "Green (2)" -> "Green")
    artist = re.sub(r'\s*\(\d+\)\s*', '', artist).strip()
    
    return artist
