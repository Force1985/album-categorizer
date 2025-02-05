"""
Info format transformations
"""

def transform_info_format(qty: str, name: str, descriptions: list[str], text: str = '') -> str:
    """
    Transform format information for info panel display
    
    Args:
        qty: Quantity of the format
        name: Name of the format
        descriptions: List of format descriptions
        text: Additional format text information
        
    Returns:
        Formatted string like "2x File, FLAC, EP" or "File, FLAC, EP" if qty is 1
    """
    if not name:
        return ''
        
    # Convert qty to int, default to 1 if not valid
    try:
        qty_num = int(qty)
    except (ValueError, TypeError):
        qty_num = 1
        
    # Build the base format string
    if qty_num > 1:
        format_str = f'{qty_num}x{name}'
    else:
        format_str = name
        
    # Add descriptions if present
    if descriptions:
        format_str += ', ' + ', '.join(descriptions)
        
    # Add text if present
    if text:
        format_str += f', {text}'
        
    return format_str
