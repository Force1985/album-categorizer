"""
Artist name transformations
"""
import re

def transform_artist(artist: str) -> str:
    """
    Transform a single artist name
    
    Args:
        artist: Artist name string
        
    Returns:
        Transformed artist name
    """
    if not artist:
        return artist
        
    # Check for Various Artists variations
    if artist.lower() in ['various', 'various artists', 'v/a', 'va']:
        return 'VA'
    
    # Remove numbers in parentheses (e.g., "Green (2)" -> "Green")
    artist = re.sub(r'\s*\(\d+\)\s*', '', artist).strip()
    
    return artist
