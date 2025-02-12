"""
URL input component
"""
import streamlit as st
from ..api.discogs import fetch_discogs_data
from ..utils.file_operations import create_album_folder

def render_url_input():
    """Render the URL input component"""

    # Main grid
    col1, col2 = st.columns([16, 5], vertical_alignment="bottom")

    with col1:
        # Input field
        discogs_url = st.text_input(
            label="Discogs URL",
            placeholder="https://www.discogs.com/release/...",
            help="Paste a Discogs album URL here",
            key="url_input",
            value="https://www.discogs.com/release/139061-DJ-Antoine-Visit-Me"
            # value="https://www.discogs.com/release/6817-DJ-Slip-Outward-EP"
        )

    with col2:
        # Fetch button
        fetch_button = st.button(
            "Fetch Data",
            type="primary",
            help="Fetch album data from Discogs",
            use_container_width=True
        )

    return discogs_url, fetch_button
