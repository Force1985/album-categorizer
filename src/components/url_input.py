import streamlit as st
from ..api.discogs import fetch_discogs_data
from ..utils.file_operations import create_album_folder

def render_url_input():
    """Render the URL input component"""
    # Create a row for the input field and button using columns
    col1, col2 = st.columns([16, 5], vertical_alignment="bottom") # 16:5 ratio for input:separator:button

    # Input field in the first (wider) column
    with col1:
        discogs_url = st.text_input(
            label="Discogs URL",
            placeholder="https://www.discogs.com/release/...",
            help="Paste a Discogs album URL here",
            key="url_input",
            value="https://www.discogs.com/release/139061-DJ-Antoine-Visit-Me"
        )

    # Button in the second (narrower) column
    with col2:
        fetch_button = st.button(
            "Fetch Data",
            type="primary",
            help="Fetch album data from Discogs",
            use_container_width=True
        )

    return discogs_url, fetch_button
