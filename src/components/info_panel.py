import streamlit as st
from ..transformations.info import transform_info_artist

def render_info_panel():
    """
    Renders the information panel component that displays album and collection details.
    """
    with st.container():
        st.subheader('Album Information')
        
        # Create columns for the input fields
        col1, sep1, col2, sep2, col3, sep3, col4 = st.columns([10, 1, 10, 1, 10, 1, 10])

        with col1:
            info_artist = st.text_input(
                f"Artist (API: {st.session_state.original_artists_sort})" if 'original_artists_sort' in st.session_state else "Artist",
                value=transform_info_artist(st.session_state.get('original_artists_sort', '')),
                key="info_artist"
            )
        with sep1:
            st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
        with col2:
            info_title = st.text_input(
                f"Title (API: {st.session_state.original_title})" if 'original_title' in st.session_state else "Title",
                value=st.session_state.get('original_title', ''),
                key="info_title"
            )
        with sep2:
            st.markdown("<div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div></div>", unsafe_allow_html=True)
        with sep3:
            st.markdown("<div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div></div>", unsafe_allow_html=True)
        
        template = f"""{st.session_state.info_artist} - {st.session_state.info_title}

Label: [labels.name]
Catalog#: [labels.catno]
Format: [formats.qty]x[formats.name], [formats.descriptions]
Country: [country]
Released: [released]
Style: [styles]
Notes: Written & produced by ???.
[notes]
Discogs: [uri]

Tracklist:
[tracklist.position]. {st.session_state.info_artist} - [tracklist.title]    [tracklist.duration]
    [extraartists.role] - [extraartists.name]"""

        st.text_area(
            label="Info Template",
            value=template,
            height=400,
            disabled=True
        )
