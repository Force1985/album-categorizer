"""
Streaming Services Component
"""
import streamlit as st
from src.api.spotify import init_spotify_api

def init_streaming_state():
    """Initialize streaming services related session state variables"""
    if 'spotify_search_results' not in st.session_state:
        st.session_state.spotify_search_results = None

def search_spotify_album():
    """Search for album on Spotify using Discogs data"""
    # Get Discogs data from session state
    artist = st.session_state.original_artist
    title = st.session_state.original_title
    
    if not artist or not title:
        st.error('Album data not found')
        return
        
    # Create search query
    query = f'artist:{artist} album:{title}'
    
    # Search on Spotify
    spotify = init_spotify_api()
    if not spotify:
        st.error('Failed to connect to Spotify. Please check your credentials in Settings.')
        return
        
    albums, error = spotify.search_album(query)
    if error:
        st.error(f'Failed to search Spotify: {error}')
    else:
        st.session_state.spotify_search_results = albums



def render_spotify_results():
    """Render Spotify search results"""
    if not st.session_state.spotify_search_results:
        return
    
    for album in st.session_state.spotify_search_results:
        with st.container():
            col1, col2, col3 = st.columns([3, 14, 5], vertical_alignment="center")
            
            # Album cover
            with col1:
                images = album.get('images', [])
                if images:
                    st.image(images[0]['url'], width=100)
            
            # Album details
            with col2:
                # Artist and album info
                artists = album.get('artists', [])
                artist_names = ', '.join(artist['name'] for artist in artists)
                if album.get('release_date'):
                    release_date = album["release_date"]
                if album.get('total_tracks'):
                    total_tracks = album["total_tracks"]
                st.info(
                    f'**{artist_names}** - {album.get("name")}  \nReleased: {release_date}  \nTracks: {total_tracks}'
                )
            
            # Artist details
            with col3:
                # Album button
                if album.get('external_urls', {}).get('spotify'):
                    st.markdown(
                        f'<a href="{album["external_urls"]["spotify"]}" target="_blank" class="stButton-fake">Open Album</a>', 
                        unsafe_allow_html=True
                    )
                # Artist button
                if artists and artists[0].get('external_urls', {}).get('spotify'):
                    st.markdown(
                        f'<a href="{artists[0]["external_urls"]["spotify"]}" target="_blank" class="stButton-fake">Open Artist</a>', 
                        unsafe_allow_html=True
                    )

def render_streaming_services():
    """
    Renders the streaming services component that displays Spotify and Tidal integration options.
    """
    init_streaming_state()
    
    with st.container():
        st.subheader('Streaming Services')

        main_col1, main_sep, main_col2 = st.columns([20, 1, 20])
        
        with main_col1:
            # Spotify section

            # Check if Spotify credentials are available
            if not (st.session_state.spotify_client_id and st.session_state.spotify_client_secret):
                st.warning('Please provide your Spotify API credentials in Settings.')
            else:
                # Show search button if we have album data
                has_album = (
                    'original_artist' in st.session_state and
                    'original_title' in st.session_state
                )
                
                if not has_album:
                    st.info('Load an album first to search on Spotify')
                else:
                    col1, col2 = st.columns([8, 4], vertical_alignment="center")

                    with col1:
                        st.markdown('##### Spotify')

                    with col2:
                        if st.button(
                            'Search this album on Spotify',
                            key='spotify_search',
                            use_container_width=True
                        ):
                            search_spotify_album()
                    
                    # Display search results
                    if st.session_state.spotify_search_results:
                        render_spotify_results()
            
        with main_sep:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)

        with main_col2:
            # Tidal section (placeholder)
            st.markdown('##### Tidal')
            st.info('Coming soon...')

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
