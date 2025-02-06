import streamlit as st
from ..utils.file_operations import create_album_folder

def update_combined_output(label, catalog, artist, title):
    """Update the combined output when any input changes"""
    return f"{label} {catalog} - {artist} - {title}"

def render_folder_output():
    """Render the folder output component"""

    # File/Folder Name Section - only show if we have API response
    st.subheader("File / Folder Name")

    # Main grid - 3 columns (21-1-21)
    main_col1, main_sep, main_col2 = st.columns([21, 1, 21])

    with main_col1:
        # First row in the nested grid
        col1, sep1, col2 = st.columns([10, 1, 10])

        with col1:
            label = st.text_input(
                f"Label / API: {st.session_state.original_label}" if st.session_state.original_label else "Label",
                key="label"
            )
        with sep1:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
        with col2:
            catalog = st.text_input(
                f"Catalog# / API: {st.session_state.original_catalog}" if st.session_state.original_catalog else "Catalog#",
                key="catalog"
            )

        # Second row in the nested grid
        col3, sep2, col4 = st.columns([10, 1, 10])

        with col3:
            artist = st.text_input(
                f"Artist / API: {st.session_state.original_artist}" if st.session_state.original_artist else "Artist",
                key="artist"
            )
        with sep2:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
        with col4:
            title = st.text_input(
                f"Title / API: {st.session_state.original_title}" if st.session_state.original_title else "Title",
                key="title"
            )

    with main_sep:
        st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
    with main_col2:
        combined_output = st.text_input(
            "Preview",
            value=update_combined_output(label, catalog, artist, title),
            disabled=True,
            key="combined_output"
        )

        st.markdown("<div class='separator-label'> </div>", unsafe_allow_html=True)
        
        if st.button(
            "Save Folder",
            key="save_folder_btn",
            type="secondary",
            help="Create a folder for the album in the export directory",
            use_container_width=True
        ): create_album_folder(combined_output)
    
    st.markdown("<div class='separator-line'></div>", unsafe_allow_html=True)
