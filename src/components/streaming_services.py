"""
Streaming Services Component
"""
import streamlit as st
from src.api.spotify import init_spotify_api

def init_streaming_state():
    """Initialize streaming services related session state variables"""
    if 'spotify_client_id' not in st.session_state:
        st.session_state.spotify_client_id = ''
    if 'spotify_client_secret' not in st.session_state:
        st.session_state.spotify_client_secret = ''
    if 'spotify_connected' not in st.session_state:
        st.session_state.spotify_connected = False
    if 'spotify_search_results' not in st.session_state:
        st.session_state.spotify_search_results = None

def handle_spotify_connect():
    """Handle Spotify connect button click"""
    spotify = init_spotify_api()
    if spotify:
        # Test connection by getting access token
        access_token = spotify.get_access_token()
        if access_token:
            st.session_state.spotify_connected = True
            st.success('Successfully connected to Spotify!')
        else:
            st.error('Failed to connect to Spotify. Please check your credentials.')
    else:
        st.error('Please enter your Spotify credentials first.')

def handle_spotify_disconnect():
    """Handle Spotify disconnect button click"""
    st.session_state.spotify_connected = False
    st.session_state.spotify_client_id = ''
    st.session_state.spotify_client_secret = ''
    st.session_state.spotify_search_results = None
    st.success('Disconnected from Spotify.')

def search_spotify_album():
    """Search for album on Spotify using Discogs data"""
    if not st.session_state.spotify_connected:
        return
        
    # Get Discogs data from session state
    artists_sort = st.session_state.get('original_artists_sort')
    title = st.session_state.get('original_title')
    
    if not artists_sort or not title:
        return
        
    # Create search query
    query = f'artist:{artists_sort} album:{title}'
    
    # Search on Spotify
    spotify = init_spotify_api()
    if spotify:
        albums, error = spotify.search_album(query)
        if error:
            st.error(f'Failed to search Spotify: {error}')
        else:
            st.session_state.spotify_search_results = albums

def render_spotify_results():
    """Render Spotify search results"""
    if not st.session_state.spotify_search_results:
        return
        
    st.markdown('#### Found on Spotify')
    
    for album in st.session_state.spotify_search_results:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            # Album cover
            with col1:
                images = album.get('images', [])
                if images:
                    st.image(images[0]['url'], width=100)
            
            # Album details
            with col2:
                artists = ', '.join(artist['name'] for artist in album.get('artists', []))
                st.markdown(f'**{artists}** - {album.get("name")}')
                
                # Additional details
                details = []
                if album.get('release_date'):
                    details.append(f'Released: {album["release_date"]}')
                if album.get('total_tracks'):
                    details.append(f'Tracks: {album["total_tracks"]}')
                if album.get('external_urls', {}).get('spotify'):
                    details.append(f'[Open in Spotify]({album["external_urls"]["spotify"]})')
                
                st.markdown(' | '.join(details))

def render_streaming_services():
    """
    Renders the streaming services component that displays Spotify and Tidal integration options.
    """
    init_streaming_state()
    
    with st.container():
        st.subheader('Streaming Services')
        
        # Spotify section
        st.markdown('#### Spotify')
        
        # Spotify credentials input
        if not st.session_state.spotify_connected:
            col1, col2 = st.columns(2)
            with col1:
                client_id = st.text_input(
                    'Client ID',
                    value=st.session_state.spotify_client_id,
                    type='password',
                    key='spotify_client_id_input'
                )
                st.session_state.spotify_client_id = client_id
            
            with col2:
                client_secret = st.text_input(
                    'Client Secret',
                    value=st.session_state.spotify_client_secret,
                    type='password',
                    key='spotify_client_secret_input'
                )
                st.session_state.spotify_client_secret = client_secret
        
        # Spotify connection buttons
        col3, col4 = st.columns(2)
        with col3:
            if st.button(
                'Connect Spotify',
                key='spotify_connect',
                disabled=st.session_state.spotify_connected
            ):
                handle_spotify_connect()
                if st.session_state.spotify_connected:
                    search_spotify_album()
        with col4:
            if st.button(
                'Disconnect',
                key='spotify_disconnect',
                disabled=not st.session_state.spotify_connected
            ):
                handle_spotify_disconnect()
        
        # Display Spotify search results
        if st.session_state.spotify_connected:
            render_spotify_results()
            
        # Tidal section
        st.markdown('#### Tidal')
        col5, col6 = st.columns(2)
        with col5:
            st.button('Connect Tidal', key='tidal_connect')
        with col6:
            st.button('Disconnect', key='tidal_disconnect', disabled=True)

    st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)

def get_spotify_data():
    """
    Retrieves data from Spotify API.
    This is a placeholder function for future implementation.
    """
    pass

def get_tidal_data():
    """
    Retrieves data from Tidal API.
    This is a placeholder function for future implementation.
    """
    pass
