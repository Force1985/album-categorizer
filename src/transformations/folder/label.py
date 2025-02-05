"""
Label name transformations
"""
import re

def transform_label(label_name: str) -> str:
    """
    Transform label name by removing common suffixes like 'Records' or 'Recordings'
    and numbers in parentheses
    
    Args:
        label_name: Original label name from Discogs API
        
    Returns:
        Transformed label name
    """
    if not label_name:
        return label_name
        
    # Remove numbers in parentheses (e.g., "Global Underground (3)" -> "Global Underground")
    label_name = re.sub(r'\s*\(\d+\)\s*', '', label_name).strip()
        
    # List of suffixes to remove (case insensitive)
    suffixes = [' records', ' recordings']
    
    # Convert to lower case for comparison
    label_lower = label_name.lower()
    
    # Check each suffix
    for suffix in suffixes:
        if label_lower.endswith(suffix):
            # Remove the suffix from the original string (preserving original case)
            return label_name[:-len(suffix)].strip()
            
    return label_name.strip()

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
    
    # Handle special cases where label might be abbreviated differently
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
