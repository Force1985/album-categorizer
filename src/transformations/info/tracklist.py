"""
Tracklist transformations for info panel
"""
import re
from typing import List, Dict, Optional

def transform_track_artist(artist: str) -> str:
    """
    Transform track artist name
    
    Args:
        artist: Track artist name from API
        
    Returns:
        Transformed track artist name
    """
    if not artist:
        return ''
        
    # Handle Various Artists variations
    if artist.lower() in ['various', 'various artists', 'v/a', 'va']:
        return 'Various Artists'
    
    # Remove numbers in parentheses (e.g., "Green (2)" -> "Green")
    artist = re.sub(r'\s*\(\d+\)\s*', '', artist).strip()
    
    return artist

def transform_track_title(title: str) -> str:
    """
    Transform track title
    
    Args:
        title: Track title from API
        
    Returns:
        Transformed track title
    """
    if not title:
        return ''
    
    # Remove numbers in parentheses
    title = re.sub(r'\s*\(\d+\)\s*', '', title).strip()
    
    return title

def transform_track_duration(duration: str) -> str:
    """
    Transform track duration
    
    Args:
        duration: Track duration from API
        
    Returns:
        Transformed track duration
    """
    if not duration:
        return ''
    
    return duration.strip()

def transform_track_extra_artists(extra_artists: List[Dict]) -> List[Dict[str, str]]:
    """
    Transform track extra artists
    
    Args:
        extra_artists: List of extra artists from API
        
    Returns:
        List of transformed extra artists with role and name
    """
    if not extra_artists:
        return []
    
    transformed = []
    for artist in extra_artists:
        name = artist.get('name', '').strip()
        role = artist.get('role', '').strip()
        
        if name and role:
            # Remove numbers in parentheses from name
            name = re.sub(r'\s*\(\d+\)\s*', '', name).strip()
            transformed.append({
                'name': name,
                'role': role
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
