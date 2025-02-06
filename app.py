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
for key in ['label', 'catalog', 'artist', 'title', 'country', 'formats_qty', 'formats_name', 'format_text', 'format_descriptions', 'released', 'style', 'notes', 'discogs_url']:
    if key not in st.session_state:
        st.session_state[key] = ''
    if f'original_{key}' not in st.session_state:
        st.session_state[f'original_{key}'] = ''

# Initialize list type session state variables
for key in ['format_descriptions']:
    if key not in st.session_state:
        st.session_state[key] = []

# Main title and description
st.markdown("<h1 class='custom-title'>Album Categorizer <span>♪</span></h1>", unsafe_allow_html=True)
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
            raw_country = data.get('country', '')

            # Get format information
            formats = data.get('formats', [{}])
            raw_format_qty = formats[0].get('qty', '')
            raw_format_name = formats[0].get('name', '')
            raw_format_descriptions = formats[0].get('descriptions', [])
            raw_format_text = formats[0].get('text', '')
            raw_released = data.get('released', '')
            raw_styles = ', '.join(data.get('styles', []))
            raw_notes = data.get('notes', '')

            # Store original values in session state
            st.session_state.original_label = raw_label
            st.session_state.original_catalog = raw_catalog
            st.session_state.original_artist = raw_artist
            st.session_state.original_title = raw_title
            st.session_state.original_artists_sort = raw_artists_sort
            st.session_state.original_formats_qty = raw_format_qty
            st.session_state.original_formats_name = raw_format_name
            st.session_state.original_format_descriptions = raw_format_descriptions
            st.session_state.original_format_text = raw_format_text
            st.session_state.original_country = raw_country
            st.session_state.original_released = raw_released
            st.session_state.original_style = raw_styles
            st.session_state.original_notes = raw_notes
            st.session_state.original_discogs_url = discogs_url

            # Apply transformations and update current values
            st.session_state.label = transform_label(raw_label)
            st.session_state.catalog = transform_catalog(raw_catalog, raw_label)
            st.session_state.artist = transform_artist(input_artist, raw_format_descriptions)
            st.session_state.title = transform_title(raw_title, raw_format_descriptions, input_artist)
            st.session_state.formats_qty = raw_format_qty
            st.session_state.formats_name = raw_format_name
            st.session_state.format_descriptions = raw_format_descriptions
            st.session_state.format_text = raw_format_text
            st.session_state.country = raw_country
            st.session_state.released = raw_released
            st.session_state.style = raw_styles
            st.session_state.notes = raw_notes
            st.session_state.discogs_url = discogs_url

# API Response Debug Section (always visible if we have a response)
if st.session_state.api_response:
    with st.expander("🔍 View API Response Details"):
        st.json(st.session_state.api_response)

    # Load global CSS
    with open('static/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Render folder output component
    render_folder_output()
    render_info_panel()
