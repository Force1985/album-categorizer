"""
Info notes transformations
"""
import re
import requests

DISCOGS_USER_AGENT = "AlbumCategorizer/1.0"

def get_artist_details(resource_url: str) -> tuple[str, list[str]]:
    """
    Fetch artist's details from Discogs API
    
    Args:
        resource_url: Artist's resource URL from Discogs API
        
    Returns:
        Tuple of (realname, list of member names)
    """
    try:
        headers = {'User-Agent': DISCOGS_USER_AGENT}
        response = requests.get(resource_url, headers=headers)
        response.raise_for_status()
        artist_data = response.json()
        
        realname = artist_data.get('realname', '')
        members = [member.get('name', '') for member in artist_data.get('members', [])]
        # Filter out empty member names
        members = [name for name in members if name]
        
        return realname, members
    except:
        return '', []

def format_artist_with_details(artist_name: str, resource_url: str) -> str:
    """
    Format artist name with real name or member names if available
    
    Args:
        artist_name: Artist's display name
        resource_url: Artist's resource URL from Discogs API
        
    Returns:
        Formatted artist name, potentially with real name or members in parentheses
    """
    realname, members = get_artist_details(resource_url)
    
    # If we have a realname and it's different from the artist name, use that
    if realname and realname.strip() != artist_name.strip():
        return f"{artist_name} ({realname})"
    # If we have members, use those
    elif members:
        return f"{artist_name} ({', '.join(members)})"
    # Otherwise just return the artist name
    return artist_name

def remove_bbcode_urls(text: str) -> str:
    """
    Remove BBCode URL tags from text and keep only the link text.
    
    Args:
        text: Text containing BBCode URL tags
        
    Returns:
        Text with URL tags removed, keeping only the link text
    """
    if not text:
        return ''
    
    # Pattern to match BBCode URL tags: [url=...]text[/url]
    pattern = r'\[url=.*?\](.*?)\[/url\]'
    return re.sub(pattern, r'\1', text)

def transform_info_notes(notes: str, artist: str, format_descriptions: list[str], api_response: dict = None) -> str:
    """
    Transform notes text based on format descriptions
    
    Args:
        notes: Original notes text from API
        artist: Artist name (comma separated if multiple)
        format_descriptions: List of format descriptions from API
        api_response: Full Discogs API response containing artist details
        
    Returns:
        Transformed notes with artist credit line and URLs removed
    """
    if not artist:
        return remove_bbcode_urls(notes) if notes else ''
        
    # Check if 'Mixed' is in format descriptions
    is_mixed = any(desc.lower() == 'mixed' for desc in format_descriptions)
    
    # Format each artist name with their details if available
    formatted_artists = []
    if api_response and 'artists' in api_response:
        for artist_data in api_response['artists']:
            artist_name = artist_data.get('name', '')
            resource_url = artist_data.get('resource_url', '')
            if artist_name and resource_url:
                formatted_artists.append(format_artist_with_details(artist_name, resource_url))
    
    # If we couldn't get formatted artists (e.g. no API response), use original artist string
    if not formatted_artists:
        formatted_artists = [artist]
    
    # Join artists with commas
    formatted_artist_string = ', '.join(formatted_artists)

    # Handle Various Artists variations
    if formatted_artist_string.lower() in ['various', 'various artists', 'v/a', 'va']:
        formatted_artist_string = 'Various Artists'
    
    # Create credit line based on format
    credit_line = f"Mixed by {formatted_artist_string}." if is_mixed else f"Written & produced by {formatted_artist_string}."
    
    # Store credit line in session state for use in comment field
    import streamlit as st
    st.session_state['info_credit_line'] = credit_line
    
    # Combine credit line with original notes, removing URLs from notes
    if notes:
        cleaned_notes = remove_bbcode_urls(notes)
        return f"{credit_line}\n{cleaned_notes}"
    return credit_line
