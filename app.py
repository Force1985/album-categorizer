import streamlit as st
import requests
import re
import json
from urllib.parse import urlparse

# Page configuration
st.set_page_config(
    page_title="Album Categorizer",
    page_icon="🎵",
    layout="centered"
)

# Initialize session state
if 'previous_url' not in st.session_state:
    st.session_state.previous_url = ''

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
        key="url_input"
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
            with st.expander(" View API Response Details"):
                st.json(response.json())

            # Display album information
            st.subheader("Album Information")
            
            # Basic info
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Title:**", data.get('title', 'N/A'))
                st.write("**Artist:**", data.get('artists', [{}])[0].get('name', 'N/A'))
                st.write("**Year:**", data.get('year', 'N/A'))
                st.write("**Label:**", data.get('labels', [{}])[0].get('name', 'N/A'))
            
            with col2:
                st.write("**Format:**", data.get('formats', [{}])[0].get('name', 'N/A'))
                st.write("**Country:**", data.get('country', 'N/A'))
                st.write("**Genre:**", ", ".join(data.get('genres', ['N/A'])))
                st.write("**Style:**", ", ".join(data.get('styles', ['N/A'])))
            
            # Tracklist
            st.subheader("Tracklist")
            for track in data.get('tracklist', []):
                st.write(f"- {track.get('position', '')} {track.get('title', 'N/A')} ({track.get('duration', 'N/A')})")