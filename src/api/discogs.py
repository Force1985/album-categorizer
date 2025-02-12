"""
Discogs API integration module
"""
import requests
import re

DISCOGS_API_URL = "https://api.discogs.com"
DISCOGS_USER_AGENT = "AlbumCategorizer/1.0"

def extract_release_id(url):
    """Extract release ID from Discogs URL"""
    pattern = r'release/(\d+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_discogs_data(url):
    """Fetch album data from Discogs API"""
    release_id = extract_release_id(url)
    if not release_id:
        return None, None, "Invalid Discogs URL. Please use a release URL (e.g., https://www.discogs.com/release/123)"

    headers = {
        'User-Agent': DISCOGS_USER_AGENT
    }
    
    try:
        response = requests.get(
            f"{DISCOGS_API_URL}/releases/{release_id}",
            headers=headers
        )
        response.raise_for_status()
        return response.json(), response, None
    except requests.exceptions.RequestException as e:
        return None, None, f"Error fetching data: {str(e)}"
