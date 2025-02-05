"""
Info notes transformations
"""

def transform_info_notes_label(notes: str, max_length: int = 100) -> str:
    """
    Transform notes text for label display by truncating if too long
    
    Args:
        notes: Notes text to transform
        max_length: Maximum length of the text before truncation
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if not notes:
        return ''
        
    if len(notes) <= max_length:
        return notes
        
    return notes[:max_length] + '...'
