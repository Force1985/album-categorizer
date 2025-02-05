"""
Info notes transformations
"""

def transform_info_notes(notes: str, artist: str, format_descriptions: list[str]) -> str:
    """
    Transform notes text based on format descriptions
    
    Args:
        notes: Original notes text from API
        artist: Artist name
        format_descriptions: List of format descriptions from API
        
    Returns:
        Transformed notes with artist credit line
    """
    if not artist:
        return notes if notes else ''
        
    # Check if 'Mixed' is in format descriptions
    is_mixed = any(desc.lower() == 'mixed' for desc in format_descriptions)
    
    # Create credit line based on format
    credit_line = f"Mixed by {artist}." if is_mixed else f"Written & produced by {artist}."
    
    # Combine credit line with original notes
    if notes:
        return f"{credit_line}\n{notes}"
    return credit_line
