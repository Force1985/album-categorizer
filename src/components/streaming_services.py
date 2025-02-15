"""
Streaming Services Component
"""
import streamlit as st
import urllib.parse

def create_search_urls(artist: str, album: str) -> tuple[str, str]:
    """
    Create search URLs for Spotify and TIDAL
    
    Args:
        artist: Artist name
        album: Album name
        
    Returns:
        Tuple of (Spotify search URL, TIDAL search URL)
    """
    search_term = f'{artist} {album}'
    encoded_term = urllib.parse.quote(search_term)
    
    spotify_url = f'https://open.spotify.com/search/{encoded_term}/albums'
    tidal_url = f'https://listen.tidal.com/search/albums?q={encoded_term}'
    
    return spotify_url, tidal_url

def render_streaming_services():
    """
    Renders the streaming services component that displays Spotify and TIDAL search links.
    """
    with st.container():
        st.subheader('Streaming Services')

        # Check if we have album data
        has_album = (
            'original_artist' in st.session_state and
            'original_title' in st.session_state
        )
        
        if has_album:
            # Create search URLs
            spotify_url, tidal_url = create_search_urls(
                st.session_state.original_artist,
                st.session_state.original_title
            )
        
        main_col1, main_sep, main_col2 = st.columns([20, 1, 20])
        
        with main_col1:
            # Spotify section
            col1, col2 = st.columns([15, 5], vertical_alignment="center")

            with col1:
                st.markdown('##### Spotify')

            with col2:      
                if not has_album:
                    st.info('Tölts be egy albumot a Spotify kereső megjelenítéséhez')
                else:
                    st.markdown(
                        f'''
                        <a href="{spotify_url}" target="_blank" class="stButton-fake">
                            Search on Spotify
                        </a>
                        ''',
                        unsafe_allow_html=True
                    )
            
        with main_sep:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)

        with main_col2:
            # TIDAL section
            col1, col2 = st.columns([15, 5], vertical_alignment="center")

            with col1:
                st.markdown('##### TIDAL')

            with col2:      
                if not has_album:
                    st.info('Tölts be egy albumot a TIDAL kereső megjelenítéséhez')
                else:
                    st.markdown(
                        f'''
                        <a href="{tidal_url}" target="_blank" class="stButton-fake">
                            Search on TIDAL
                        </a>
                        ''',
                        unsafe_allow_html=True
                    )

        st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
