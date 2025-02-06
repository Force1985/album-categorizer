"""
Info URL transformations
"""

def transform_info_url(url: str) -> str:
    """
    Transform Discogs URL to its short version
    
    Args:
        url: Original Discogs URL
        
    Returns:
        Short version of the URL containing only the release ID
    """
    if not url:
        return ''
        
    # Extract base URL and release ID
    parts = url.split('/release/')
    if len(parts) != 2:
        return url
        
    release_id = parts[1].split('-')[0]
    if not release_id.isdigit():
        return url
        
    return f"https://www.discogs.com/release/{release_id}"
