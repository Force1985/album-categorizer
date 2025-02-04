"""
Catalog number transformations
"""
import re
from .label import get_label_variations

def extract_number_part(catalog: str) -> str:
    """
    Extract the numeric part from a catalog number, preserving any trailing characters
    
    Args:
        catalog: Catalog number to process
        
    Returns:
        The numeric part with any trailing characters
    """
    # Find the first digit
    match = re.search(r'\d', catalog)
    if match:
        start_idx = match.start()
        return catalog[start_idx:]
    return catalog

def transform_catalog(catalog: str, label: str) -> str:
    """
    Transform catalog number by removing label prefix if present
    
    Args:
        catalog: Original catalog number from Discogs API
        label: Label name (possibly already transformed)
        
    Returns:
        Transformed catalog number
    """
    if not catalog or not label:
        return catalog
        
    # Convert to uppercase for comparison
    catalog_upper = catalog.upper()
    
    # Get possible label variations
    label_variations = get_label_variations(label)
    
    # Try to find and remove label prefix
    for variation in label_variations:
        # Create pattern to match variation at start, followed by optional separator
        pattern = f'^{re.escape(variation)}[-\\s]*'
        
        # Try case-insensitive match
        match = re.search(pattern, catalog_upper, re.IGNORECASE)
        if match:
            # Remove the matched prefix from the original string
            result = catalog[match.end():].strip()
            # If result starts with a separator, remove it
            result = re.sub(r'^[-\s]+', '', result)
            return result
    
    # If no label prefix found, try to extract number part
    return extract_number_part(catalog)
