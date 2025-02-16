"""
Image Gallery Component
"""
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os
from ..utils.file_operations import save_image

# Előre definiált kép típusok
IMAGE_TYPES = [
    'Front', 'Back', 'Vinyl A', 'Vinyl B', 'Vinyl C', 'Vinyl D', 'CD', 'Inside', 'Inlay', 'Cover', 'Label', 'Booklet', 'Other'
]

def init_image_state():
    """Initialize image gallery related session state variables"""
    if 'discogs_images' not in st.session_state:
        st.session_state.discogs_images = []
    if 'image_types' not in st.session_state:
        st.session_state.image_types = {}

def render_image_gallery():
    """
    Renders the image gallery component that displays Discogs images.
    Images are displayed in a grid layout with 4 columns.
    """
    init_image_state()
    
    with st.container():
        st.subheader('Album Images')
        
        if not st.session_state.discogs_images:
            st.info('Load an album from Discogs to see its images')
            return
            
        # Create 3 columns for the image grid
        cols = st.columns(4)
        
        # Distribute images across columns
        for idx, image in enumerate(st.session_state.discogs_images):
            col_idx = idx % 4  # Cycle through columns
            
            with cols[col_idx]:
                # Get image dimensions
                try:
                    headers = {
                        'User-Agent': 'AlbumCategorizer/1.0'
                    }
                    response = requests.get(image['uri'], headers=headers)
                    
                    img = Image.open(BytesIO(response.content))
                    width, height = img.size
                    resolution_text = f' ({width}x{height})'
                except Exception as e:
                    resolution_text = ''
                
                # Display image with caption and resolution if available
                caption = image.get('type', '').title() + resolution_text
                st.image(
                    image['uri'],
                    caption=caption
                )
                
                # Add type selector and save button
                col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
                with col1:
                    # Unique key for each image's type selector
                    type_key = f'image_type_{idx}'
                    selected_type = st.selectbox(
                        'Image Type',
                        options=IMAGE_TYPES,
                        key=type_key
                    )
                
                with col2:
                    if st.button(
                        'Save',
                        use_container_width=True,
                        key=f'save_btn_{idx}'):
                        # Get folder name from session state components
                        folder_name = f"{st.session_state.label} {st.session_state.catalog} - {st.session_state.artist} - {st.session_state.title}"
                        if all([st.session_state.label, st.session_state.catalog, st.session_state.artist, st.session_state.title]):
                            save_image(image['uri'], folder_name, selected_type)
                        else:
                            st.warning('Please set the album folder name first')
        
        st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
