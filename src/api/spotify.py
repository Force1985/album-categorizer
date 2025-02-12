"""
Spotify API integration module
"""
import os
import base64
import requests
from typing import Optional, Dict, Tuple, Any, List
import streamlit as st

class SpotifyAPI:
    """Handles Spotify API authentication and requests"""
    
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    API_BASE_URL = 'https://api.spotify.com/v1'
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Spotify API client
        
        Args:
            client_id: Spotify client ID
            client_secret: Spotify client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_access_token(self) -> Optional[str]:
        """
        Get Spotify access token using client credentials flow
        
        Returns:
            Access token if successful, None otherwise
        """
        # Encode client credentials
        credentials = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()
        ).decode()
        
        # Request access token
        response = requests.post(
            self.AUTH_URL,
            headers={
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'grant_type': 'client_credentials'}
        )
        
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
        
    def search_album(self, query: str, limit: int = 5) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Search for albums on Spotify
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            Tuple of (list of album data, error message)
        """
        access_token = self.get_access_token()
        if not access_token:
            return None, 'Failed to get Spotify access token'
            
        response = requests.get(
            f'{self.API_BASE_URL}/search',
            headers={'Authorization': f'Bearer {access_token}'},
            params={
                'q': query,
                'type': 'album',
                'limit': limit,
                'market': 'HU'  # Hungarian market for better relevance
            }
        )
        
        if response.status_code != 200:
            return None, f'Search failed: {response.status_code}'
            
        data = response.json()
        albums = data.get('albums', {}).get('items', [])
        
        if not albums:
            return None, 'No albums found'
        
        # Get full album details for each result
        detailed_albums = []
        for album in albums:
            album_id = album['id']
            album_response = requests.get(
                f'{self.API_BASE_URL}/albums/{album_id}',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if album_response.status_code == 200:
                detailed_albums.append(album_response.json())
            
        return detailed_albums, None

def init_spotify_api() -> Optional[SpotifyAPI]:
    """
    Initialize Spotify API client with credentials from session state
    
    Returns:
        SpotifyAPI instance if credentials are present, None otherwise
    """
    client_id = st.session_state.get('spotify_client_id')
    client_secret = st.session_state.get('spotify_client_secret')
    
    if client_id and client_secret:
        return SpotifyAPI(client_id, client_secret)
    return None
