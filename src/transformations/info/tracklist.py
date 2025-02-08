"""
Tracklist transformations for info panel
"""
import re
from typing import List, Dict, Optional
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
        # Remove numbers in parentheses (e.g., "Green (2)" -> "Green")
        artist_name = re.sub(r'\s*\(\d+\)\s*', '', artist_name).strip()
        return f"{artist_name} ({realname})"
    # If we have members, use those
    elif members:
        return f"{artist_name} ({', '.join(members)})"
    # Otherwise just return the artist name
    return artist_name

def transform_track_artist(artist: str) -> str:
    """
    Transform track artist
    
    Args:
        artist: Artist from API
        
    Returns:
        Transformed artist
    """
    if not artist:
        return ''
        
    # Handle "Various" as "Various Artists"
    if artist.lower() == 'various':
        return 'Various Artists'
        
    return artist

def transform_track_title(title: str) -> str:
    """
    Transform track title
    
    Args:
        title: Title from API
        
    Returns:
        Transformed title
    """
    return title or ''

def transform_track_duration(duration: str) -> str:
    """
    Transform track duration
    
    Args:
        duration: Duration from API
        
    Returns:
        Transformed duration
    """
    return duration or ''

def transform_track_extra_artists(extra_artists: List[Dict]) -> List[Dict[str, str]]:
    """
    Transform track extra artists
    
    Args:
        extra_artists: Extra artists from API
        
    Returns:
        List of transformed extra artists with role and name
    """
    if not extra_artists:
        return []
        
    transformed = []
    for artist in extra_artists:
        name = artist.get('name', '')
        role = artist.get('role', '')
        
        # For Remix role, fetch and add artist details
        if role == 'Remix' and name and artist.get('resource_url'):
            name = format_artist_with_details(name, artist['resource_url'])
            
        if name and role:
            transformed.append({
                'role': role,
                'name': name
            })
    
    return transformed

def transform_track(track_data: Dict, album_artist: str = '') -> Dict[str, any]:
    """
    Transform a single track's data
    
    Args:
        track_data: Track data from API
        album_artist: Album's main artist, used as fallback if track has no specific artists
        
    Returns:
        Transformed track data
    """
    position = track_data.get('position', '')
    
    if position:
        # Try to convert position to number and pad with zeros if possible
        try:
            position_num = int(position)
            position = f"{position_num:02d}"
        except (ValueError, TypeError):
            # Check if position is a single letter (e.g., 'A', 'B')
            if len(position) == 1 and position.isalpha():
                position = f"{position}1"
            # If position is in any other format (e.g., "A1", "B2"), leave it as is
    
    # Handle track artists
    artists = track_data.get('artists', [])
    if artists:
        # If track has specific artists, join their names
        artist = ', '.join(artist.get('name', '') for artist in artists if artist.get('name'))
    else:
        # If no track-specific artists, use the track's artist field or fall back to album artist
        artist = track_data.get('artist', '') or album_artist
    
    return {
        'position': position,
        'artist': transform_track_artist(artist),
        'title': transform_track_title(track_data.get('title', '')),
        'duration': transform_track_duration(track_data.get('duration', '')),
        'extra_artists': transform_track_extra_artists(track_data.get('extraartists', []))
    }

def transform_info_tracklist(tracklist: List[Dict], album_artist: str = '') -> List[Dict[str, any]]:
    """
    Transform tracklist data for info panel
    
    Args:
        tracklist: List of tracks from API
        album_artist: Album's main artist, used as fallback if track has no specific artists
        
    Returns:
        List of transformed track data
    """
    if not tracklist:
        return []
    
    return [transform_track(track, album_artist) for track in tracklist]
