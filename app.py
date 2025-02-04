import streamlit as st
from PIL import Image
from src.transformations import (
    transform_label,
    transform_catalog,
    transform_artist,
    transform_title
)
from src.components.url_input import render_url_input
from src.components.folder_output import render_folder_output
from src.components.info_panel import render_info_panel
from src.api.discogs import fetch_discogs_data

# Load custom favicon
favicon = Image.open("static/images/favicon.ico")

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

# Render URL input component
discogs_url, fetch_button = render_url_input()

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
            raw_artist = ', '.join(artist.get('anv') or artist.get('name', '') for artist in data.get('artists', []))
            input_artist = ' & '.join(artist.get('anv') or artist.get('name', '') for artist in data.get('artists', []))
            raw_title = data.get('title', '')
            raw_artists_sort = data.get('artists_sort', '')

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
            st.session_state.original_artists_sort = raw_artists_sort

            # Apply transformations and update current values
            st.session_state.label = transform_label(raw_label)
            st.session_state.catalog = transform_catalog(raw_catalog, st.session_state.label)
            st.session_state.artist = transform_artist(input_artist)
            st.session_state.title = transform_title(raw_title, format_descriptions)

# API Response Debug Section (always visible if we have a response)
if st.session_state.api_response:
    with st.expander("🔍 View API Response Details"):
        st.json(st.session_state.api_response)

    # Render folder output component
    render_folder_output(st.session_state.api_response)
    render_info_panel()
