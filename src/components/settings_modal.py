"""
Settings Modal Component
"""
import streamlit as st
from typing import Tuple
import os
from dotenv import load_dotenv

def init_settings():
    """Initialize settings related session state variables and load from .env"""
    # Initialize session state variables if not exist
    if 'discogs_token' not in st.session_state:
        st.session_state.discogs_token = ''
    if 'spotify_client_id' not in st.session_state:
        st.session_state.spotify_client_id = ''
    if 'spotify_client_secret' not in st.session_state:
        st.session_state.spotify_client_secret = ''
    
    # Load from .env if exists
    load_dotenv()
    
    if os.getenv('DISCOGS_TOKEN'):
        st.session_state.discogs_token = os.getenv('DISCOGS_TOKEN')
    if os.getenv('SPOTIFY_CLIENT_ID'):
        st.session_state.spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
    if os.getenv('SPOTIFY_CLIENT_SECRET'):
        st.session_state.spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

def render_settings() -> None:
    """Render the settings popover"""
    with st.popover('⚙️ Settings', use_container_width=False):
        # Discogs API section
        st.markdown('#### 💿 Discogs API')
        st.markdown("""
        To get your Discogs API token:
        1. Go to [Discogs Developer Settings](https://www.discogs.com/settings/developers)
        2. Generate a new token
        3. Copy and paste it below
        """)
        
        discogs_token = st.text_input(
            'Discogs Token',
            value=st.session_state.discogs_token,
            type='password',
            key='settings_discogs_token_input'
        )
        st.session_state.discogs_token = discogs_token
        
        st.markdown('---')
        
        # Spotify API section
        st.markdown('#### 🎵 Spotify API')
        st.markdown("""
        To get your Spotify API credentials:
        1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
        2. Create a new app
        3. Copy the Client ID and Client Secret
        """)
        
        client_id = st.text_input(
            'Client ID',
            value=st.session_state.spotify_client_id,
            type='password',
            key='settings_spotify_client_id_input'
        )
        st.session_state.spotify_client_id = client_id
        
        client_secret = st.text_input(
            'Client Secret',
            value=st.session_state.spotify_client_secret,
            type='password',
            key='settings_spotify_client_secret_input'
        )
        st.session_state.spotify_client_secret = client_secret
        
        st.markdown('---')
        st.markdown("""
        💡 **Tip**: You can also set these values in a `.env` file:
        ```
        DISCOGS_TOKEN=your_token
        SPOTIFY_CLIENT_ID=your_client_id
        SPOTIFY_CLIENT_SECRET=your_client_secret
        ```
        """)
