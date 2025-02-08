"""
Label name transformations
"""
import re

def transform_info_label(label: str) -> str:
    """
    Transform label name for info panel display by removing numbers in parentheses
    
    Args:
        label: Label name string from API
        
    Returns:
        Transformed label name for info panel
    """
    if not label:
        return label
        
    # Remove numbers in parentheses (e.g., "Global Underground (3)" -> "Global Underground")
    return re.sub(r'\s*\(\d+\)\s*', '', label).strip()
