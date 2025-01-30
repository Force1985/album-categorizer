import streamlit as st
import requests
import re
import json
from urllib.parse import urlparse

# Page configuration
st.set_page_config(
    page_title="Album Categorizer",
    page_icon="🎵",
    layout="wide"
)

# Initialize session state
if 'previous_url' not in st.session_state:
    st.session_state.previous_url = ''

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
st.title("Album Categorizer 🎵")
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
        else:
            # API Response Debug Section
            with st.expander("🔍 View API Response Details"):
                st.json(response.json())

            # Update session state with new values
            label_value = data.get('labels', [{}])[0].get('name', '')
            catalog_value = data.get('labels', [{}])[0].get('catno', '')
            artist_value = data.get('artists', [{}])[0].get('name', '')
            title_value = data.get('title', '')

            st.session_state.label = label_value
            st.session_state.catalog = catalog_value
            st.session_state.artist = artist_value
            st.session_state.title = title_value

            # Store original values
            st.session_state.original_label = label_value
            st.session_state.original_catalog = catalog_value
            st.session_state.original_artist = artist_value
            st.session_state.original_title = title_value

# File/Folder Name Section
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

# Combined output field
st.text_input(
    "Combined Name",
    value=update_combined_output(),
    disabled=True,
    key="combined_output"
)