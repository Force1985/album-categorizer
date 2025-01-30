"""
Artist name transformations
"""
import re

def transform_artist(artist: str) -> str:
    """
    Transform a single artist name
    
    Args:
        artist: Single artist name from Discogs API
        
    Returns:
        Transformed artist name
    """
    if not artist:
        return artist
        
    # Check for Various Artists variations
    if artist.lower() in ['various', 'various artists', 'v/a', 'va']:
        return 'VA'
    
    return artist
