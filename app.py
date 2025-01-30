import streamlit as st
import requests
import re
import json
from urllib.parse import urlparse
from PIL import Image
from transformations import (
    transform_label,
    transform_catalog,
    transform_artist,
    transform_title
)
import os

# Load custom favicon
favicon = Image.open("favicon.ico")

# Page configuration
st.set_page_config(
    page_title="Album Categorizer",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if 'previous_url' not in st.session_state:
    st.session_state.previous_url = ''
if 'api_response' not in st.session_state:
    st.session_state.api_response = None

# Initialize input fields and original values in session state
for key in ['label', 'catalog', 'artist', 'title']:
    if key not in st.session_state:
        st.session_state[key] = ''
    if f'original_{key}' not in st.session_state:
        st.session_state[f'original_{key}'] = ''

def update_combined_output():
    """Update the combined output when any input changes"""
    return f"{st.session_state.label} {st.session_state.catalog} - {st.session_state.artist} - {st.session_state.title}"

# Discogs API configuration
DISCOGS_API_URL = "https://api.discogs.com"
DISCOGS_USER_AGENT = "AlbumCategorizer/1.0"

def extract_release_id(url):
    """Extract release ID from Discogs URL"""
    pattern = r'release/(\d+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_discogs_data(url):
    """Fetch album data from Discogs API"""
    release_id = extract_release_id(url)
    if not release_id:
        return None, None, "Invalid Discogs URL. Please use a release URL (e.g., https://www.discogs.com/release/123)"

    headers = {
        'User-Agent': DISCOGS_USER_AGENT
    }
    
    try:
        response = requests.get(
            f"{DISCOGS_API_URL}/releases/{release_id}",
            headers=headers
        )
        response.raise_for_status()
        return response.json(), response, None
    except requests.exceptions.RequestException as e:
        return None, None, f"Error fetching data: {str(e)}"

# Main title and description
st.markdown("""
    <style>
        .custom-title {
            font-family: "Source Sans Pro", sans-serif;
            font-size: 2.25rem;
            font-weight: 700;
            color: rgb(49, 51, 63);
        }
        .custom-title span {
            color: #ff4b4b;
        }
    </style>
    <h1 class="custom-title">Album Categorizer <span>♪</span></h1>
""", unsafe_allow_html=True)
st.write("Fetch and organize your favorite albums from Discogs with ease.")

# Create a row for the input field and button using columns
col1, col2 = st.columns([4, 1], vertical_alignment="bottom")  # 4:1 ratio for input:button

# Input field in the first (wider) column
with col1:
    discogs_url = st.text_input(
        label="Discogs URL",
        placeholder="https://www.discogs.com/release/...",
        help="Paste a Discogs album URL here",
        key="url_input",
        # Don't delete the following line
        value="https://www.discogs.com/release/5887661-Hironori-Takahashi-Blending-Mode-EP"
    )

# Button in the second (narrower) column
with col2:
    fetch_button = st.button("Fetch Data", type="primary", use_container_width=True)

# Check if we should fetch data (either button clicked or new URL entered)
should_fetch = fetch_button or (discogs_url != st.session_state.previous_url and discogs_url)

if should_fetch:
    st.session_state.previous_url = discogs_url
    with st.spinner('Fetching album data...'):
        data, response, error = fetch_discogs_data(discogs_url)
        
        if error:
            st.error(error)
            # Clear API response on error
            st.session_state.api_response = None
        else:
            # Store API response in session state
            st.session_state.api_response = response.json()

            # Get raw values from API
            raw_label = data.get('labels', [{}])[0].get('name', '')
            raw_catalog = data.get('labels', [{}])[0].get('catno', '')
            raw_artist = ', '.join(artist.get('name', '') for artist in data.get('artists', []))
            input_artist = ' & '.join(artist.get('name', '') for artist in data.get('artists', []))
            raw_title = data.get('title', '')

            # Get format information
            formats = data.get('formats', [{}])
            format_descriptions = []
            for fmt in formats:
                # Add descriptions from the format level
                if 'descriptions' in fmt:
                    format_descriptions.extend(desc.upper() for desc in fmt.get('descriptions', []))
                # Add descriptions from the format_description level
                if 'format_description' in fmt:
                    format_descriptions.append(fmt['format_description'].upper())

            # Store original (raw) values
            st.session_state.original_label = raw_label
            st.session_state.original_catalog = raw_catalog
            st.session_state.original_artist = raw_artist
            st.session_state.original_title = raw_title

            # Apply transformations and update current values
            st.session_state.label = transform_label(raw_label)
            st.session_state.catalog = transform_catalog(raw_catalog, st.session_state.label)
            st.session_state.artist = transform_artist(input_artist)
            st.session_state.title = transform_title(raw_title, format_descriptions)

# API Response Debug Section (always visible if we have a response)
if st.session_state.api_response:
    with st.expander("🔍 View API Response Details"):
        st.json(st.session_state.api_response)

    # File/Folder Name Section - only show if we have API response
    st.subheader("File / Folder Name")

    # Create 4 columns for the input fields
    col1, sep1, col2, sep2, col3, sep3, col4 = st.columns([10, 1, 10, 1, 10, 1, 10])

    with col1:
        st.text_input(
            f"Label (API: {st.session_state.original_label})" if st.session_state.original_label else "Label",
            key="label"
        )
    with sep1:
        st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
    with col2:
        st.text_input(
            f"Catalog# (API: {st.session_state.original_catalog})" if st.session_state.original_catalog else "Catalog#",
            key="catalog"
        )
    with sep2:
        st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
    with col3:
        st.text_input(
            f"Artist (API: {st.session_state.original_artist})" if st.session_state.original_artist else "Artist",
            key="artist"
        )
    with sep3:
        st.markdown("<div style='text-align: center; padding-top: 30px;'>-</div>", unsafe_allow_html=True)
    with col4:
        st.text_input(
            f"Title (API: {st.session_state.original_title})" if st.session_state.original_title else "Title",
            key="title"
        )

    # Combined output field with Save folder button
    combined_col1, combined_col2 = st.columns([4, 1], vertical_alignment="bottom")
    with combined_col1:
        combined_output = st.text_input(
            "Combined Name",
            value=update_combined_output(),
            disabled=True,
            key="combined_output"
        )
    with combined_col2:
        if st.button("Save Folder", key="save_folder_btn", type="secondary", use_container_width=True):
            # Create export directory if it doesn't exist
            export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'export')
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            # Create the album directory inside export
            album_dir = os.path.join(export_dir, combined_output)
            if not os.path.exists(album_dir):
                os.makedirs(album_dir)
                st.toast(f"Created folder: {os.path.basename(album_dir)}", icon="✅")
            else:
                st.toast(f"Folder already exists: {os.path.basename(album_dir)}", icon="⚠️")
