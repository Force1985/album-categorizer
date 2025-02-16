"""
Streaming Services Component
"""
import streamlit as st
import urllib.parse

def create_search_urls(artist: str, album: str) -> tuple[str, str]:
    """
    Create search URLs for Spotify, TIDAL, Beatport, and Apple Music
    
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
    beatport_url = f'https://www.beatport.com/search?q={encoded_term}'
    apple_music_url = f'https://music.apple.com/hu/search?term={encoded_term}'
    
    return spotify_url, tidal_url, beatport_url, apple_music_url

def render_streaming_services():
    """
    Renders the streaming services component that displays Spotify, TIDAL, Beatport, and Apple Music search links.
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
            spotify_url, tidal_url, beatport_url, apple_music_url = create_search_urls(
                st.session_state.original_artist,
                st.session_state.original_title
            )
        
        main_col1, main_sep1, main_col2, main_sep2, main_col3, main_sep3, main_col4 = st.columns([9.5, 1, 9.5, 1, 9.5, 1, 9.5])
        
        with main_col1:
            # Spotify section
            if not has_album:
                st.info('Enter an album to search on Spotify')
            else:
                st.markdown(
                    f'''
                    <a href="{spotify_url}" target="_blank" class="stButton-fake stButton-fake--spotify">
                        Spotify Search
                    </a>
                    ''',
                    unsafe_allow_html=True
                )
            
        with main_sep1:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)

        with main_col2:
            # Tidal section
            if not has_album:
                st.info('Enter an album to search on TIDAL')
            else:
                st.markdown(
                    f'''
                    <a href="{tidal_url}" target="_blank" class="stButton-fake stButton-fake--tidal">
                        Tidal Search
                        </a>
                        ''',
                        unsafe_allow_html=True
                    )
            
        with main_sep2:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)

        with main_col3:
            # Beatport section
            if not has_album:
                st.info('Enter an album to search on Beatport')
            else:
                st.markdown(
                    f'''
                    <a href="{beatport_url}" target="_blank" class="stButton-fake stButton-fake--beatport">
                        Beatport Search
                    </a>
                    ''',
                    unsafe_allow_html=True
                )

        with main_sep3:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)

        with main_col4:
            # Apple Music section
            if not has_album:
                st.info('Enter an album to search on Apple Music')
            else:
                st.markdown(
                    f'''
                    <a href="{apple_music_url}" target="_blank" class="stButton-fake stButton-fake--apple-music">
                        Apple Music Search
                    </a>
                    ''',
                    unsafe_allow_html=True
                )

        st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
