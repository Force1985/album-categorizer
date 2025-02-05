import streamlit as st
from ..utils.file_operations import create_album_folder

def update_combined_output(label, catalog, artist, title):
    """Update the combined output when any input changes"""
    return f"{label} {catalog} - {artist} - {title}"

def render_folder_output():
    """Render the folder output component"""

    # File/Folder Name Section - only show if we have API response
    st.subheader("File / Folder Name")

    # Create 4 columns for the input fields
    col1, sep1, col2, sep2, col3, sep3, col4 = st.columns([10, 1, 10, 1, 10, 1, 10])

    with col1:
        label = st.text_input(
            f"Label / API: {st.session_state.original_label}" if st.session_state.original_label else "Label",
            key="label"
        )
    with sep1:
        st.markdown("<div class='separator'>-</div>", unsafe_allow_html=True)
    with col2:
        catalog = st.text_input(
            f"Catalog# / API: {st.session_state.original_catalog}" if st.session_state.original_catalog else "Catalog#",
            key="catalog"
        )
    with sep2:
        st.markdown("<div class='separator'>-</div>", unsafe_allow_html=True)
    with col3:
        artist = st.text_input(
            f"Artist / API: {st.session_state.original_artist}" if st.session_state.original_artist else "Artist",
            key="artist"
        )
    with sep3:
        st.markdown("<div class='separator'>-</div>", unsafe_allow_html=True)
    with col4:
        title = st.text_input(
            f"Title / API: {st.session_state.original_title}" if st.session_state.original_title else "Title",
            key="title"
        )

    # Combined output field with Save folder button
    combined_col1, combined_col2 = st.columns([4, 1], vertical_alignment="bottom")
    with combined_col1:
        combined_output = st.text_input(
            "Combined Name",
            value=update_combined_output(label, catalog, artist, title),
            disabled=True,
            key="combined_output"
        )
    with combined_col2:
        if st.button("Save Folder", key="save_folder_btn", type="secondary", use_container_width=True):
            create_album_folder(combined_output)
