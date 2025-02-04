"""
Info artist name transformations
"""
import re

def transform_info_artist(artist: str) -> str:
    """
    Transform artist name for info panel display
    
    Args:
        artist: Artist name string from API
        
    Returns:
        Transformed artist name for info panel
    """
    if not artist:
        return artist
        
    # Check for Various Artists variations
    if artist.lower() in ['various', 'various artists', 'v/a', 'va']:
        return 'Various Artists'
    
    # Remove numbers in parentheses (e.g., "Green (2)" -> "Green")
    artist = re.sub(r'\s*\(\d+\)\s*', '', artist).strip()
    
    return artist
