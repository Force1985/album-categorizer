import streamlit as st
from ..transformations.info import transform_info_artist, transform_info_format

def render_info_panel():
    """
    Renders the information panel component that displays album and collection details.
    """
    with st.container():
        st.subheader('Album Information')
        
        # First row - Artist and Title
        col1, sep1, col2, sep2, col3, sep3, col4 = st.columns([10, 1, 10, 1, 10, 1, 10])

        with col1:
            info_artist = st.text_input(
                f"Artist / API: {st.session_state.original_artists_sort}" if 'original_artists_sort' in st.session_state else "Artist",
                value=transform_info_artist(st.session_state.get('original_artists_sort', '')),
                key="info_artist"
            )
        with sep1:
            st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
        with col2:
            info_title = st.text_input(
                f"Title / API: {st.session_state.original_title}" if 'original_title' in st.session_state else "Title",
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

        # Second row - Label, Catalog#, Format, Country
        col1, sep1, col2, sep2, col3, sep3, col4 = st.columns([10, 1, 10, 1, 10, 1, 10])

        with col1:
            info_label = st.text_input(
                f"Label / API: {st.session_state.original_label}" if 'original_label' in st.session_state else "Label",
                value=st.session_state.get('original_label', ''),
                key="info_label"
            )
        with sep1:
            st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
        with col2:
            info_catalog = st.text_input(
                f"Catalog# / API: {st.session_state.original_catalog}" if 'original_catalog' in st.session_state else "Catalog#",
                value=st.session_state.get('original_catalog', ''),
                key="info_catalog"
            )
        with sep2:
            st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
        with col3:
            # Build format label parts
            format_label_parts = []
            if 'original_formats_qty' in st.session_state and st.session_state.original_formats_qty:
                format_label_parts.append(f"q: {st.session_state.original_formats_qty}")
            if 'original_formats_name' in st.session_state and st.session_state.original_formats_name:
                format_label_parts.append(f"n: {st.session_state.original_formats_name}")
            if 'original_format_descriptions' in st.session_state and st.session_state.original_format_descriptions:
                format_label_parts.append(f"d: {st.session_state.original_format_descriptions}")
            if 'original_format_text' in st.session_state and st.session_state.original_format_text:
                format_label_parts.append(f"t: {st.session_state.original_format_text}")
                
            format_label = "Format / API: " + ", ".join(format_label_parts) if format_label_parts else "Format"
            
            formatted_format = transform_info_format(
                st.session_state.get('formats_qty', ''),
                st.session_state.get('formats_name', ''),
                st.session_state.get('format_descriptions', []),
                st.session_state.get('format_text', '')
            )
            info_format = st.text_input(
                format_label,
                value=formatted_format,
                key="info_format"
            )
        with sep3:
            st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
        with col4:
            info_country = st.text_input(
                f"Country / API: {st.session_state.original_country}" if 'original_country' in st.session_state else "Country",
                value=st.session_state.get('original_country', ''),
                key="info_country"
            )
        
        template = f"""{st.session_state.info_artist} - {st.session_state.info_title}

Label: {st.session_state.info_label}
Catalog#: {st.session_state.info_catalog}
Format: {st.session_state.info_format}
Country: {st.session_state.info_country}
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
