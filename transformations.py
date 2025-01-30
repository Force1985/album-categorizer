"""
Transformations for cleaning and formatting album data
"""
import re

def transform_label(label_name: str) -> str:
    """
    Transform label name by removing common suffixes like 'Records' or 'Recordings'
    
    Args:
        label_name: Original label name from Discogs API
        
    Returns:
        Transformed label name
    """
    if not label_name:
        return label_name
        
    # List of suffixes to remove (case insensitive)
    suffixes = [' records', ' recordings']
    
    # Convert to lower case for comparison
    label_lower = label_name.lower()
    
    # Check each suffix
    for suffix in suffixes:
        if label_lower.endswith(suffix):
            # Remove the suffix from the original string (preserving original case)
            return label_name[:-len(suffix)].strip()
    
    return label_name

def get_label_variations(label: str) -> list[str]:
    """
    Generate possible variations of a label name for catalog number matching
    
    Args:
        label: Label name
        
    Returns:
        List of possible variations of the label name
    """
    if not label:
        return []
        
    variations = []
    
    # Original label
    variations.append(label)
    
    # Remove spaces
    no_spaces = label.replace(' ', '')
    variations.append(no_spaces)
    
    # First word only
    first_word = label.split()[0] if label else ''
    variations.append(first_word)
    
    # Common abbreviations (first letters of words)
    words = label.split()
    if len(words) > 1:
        abbreviation = ''.join(word[0] for word in words if word)
        variations.append(abbreviation)
    
    # Remove special characters and convert to uppercase
    clean_label = re.sub(r'[^a-zA-Z0-9]', '', label)
    variations.append(clean_label)
    
    # 5. Handle special cases where label might be abbreviated differently
    special_cases = {
        'kanzleramt': ['ka'],
        'kompakt': ['k', 'komp'],
        'drumcode': ['dc'],
        'hospital': ['nhs'],  # NHS is commonly used for Hospital Records
        'rephlex': ['rx'],
        'warp': ['war'],
        'compound': ['comp'],  # Added Compound special case
        # Add more special cases as needed
    }
    
    label_lower = label.lower()
    if label_lower in special_cases:
        variations.extend(special_cases[label_lower])
    
    # Return unique variations, sorted by length (longest first)
    # Filter out empty strings and single characters (except for special cases)
    variations = [v for v in variations if v and (len(v) > 1 or v.lower() in ['k'])]
    return sorted(set(variations), key=len, reverse=True)

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
        # Return everything from the first digit onwards
        return catalog[match.start():].strip()
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
        
    # Get possible variations of the label name
    label_variations = get_label_variations(label)
    
    # Convert to uppercase for comparison but keep original spaces
    catalog_upper = catalog.upper()
    
    # Try each label variation
    for variation in label_variations:
        variation_upper = variation.upper()
        
        # Only check at the start of the catalog number
        if catalog_upper.strip().startswith(variation_upper):
            # Get everything after the variation, preserving original spaces
            start_pos = catalog_upper.find(variation_upper)
            remaining = catalog[start_pos + len(variation_upper):]
            
            # Remove spaces at the start and end
            remaining = remaining.strip()
            
            # If what follows is a number or starts with a separator, remove the prefix
            if remaining and (remaining[0].isdigit() or remaining[0] in '-_'):
                # Remove any separators at the start
                remaining = re.sub(r'^[-_\s]+', '', remaining)
                if remaining:
                    return remaining
            
            # Special case: if it's a format specifier (like LP, EP) after the prefix
            format_match = re.match(r'^(LP|EP)\s*(\d.*)', remaining, re.IGNORECASE)
            if format_match:
                format_type = format_match.group(1)
                number_part = format_match.group(2)
                # Add a space between format and number if there isn't one
                return f"{format_type} {number_part.strip()}"
    
    return catalog

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
