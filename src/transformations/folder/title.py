"""
Title transformations
"""
import re

def transform_title(title: str, format_descriptions: list[str] = None) -> str:
    """
    Transform album title, optionally adding format information
    
    Args:
        title: Album title from Discogs API
        format_descriptions: List of format descriptions from Discogs API
        
    Returns:
        Transformed title
    """
    if not title:
        return title
        
    # Replace colons with dashes for file system compatibility
    title = title.replace(':', ' -')
        
    # If no format descriptions provided, return original title
    if not format_descriptions:
        return title
        
    # Convert title to upper for comparison
    title_upper = title.upper()
    
    # Check for EP
    is_ep = any(desc.upper() == 'EP' for desc in format_descriptions)
    if is_ep and not title_upper.endswith('EP'):
        return f"{title} EP"
    
    # Check for LP
    is_lp = any(desc.upper() == 'LP' for desc in format_descriptions)
    if is_lp and not title_upper.endswith('LP'):
        return f"{title} LP"
    
    return title
