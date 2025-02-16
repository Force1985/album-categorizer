"""
Image Gallery Component
"""
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def init_image_state():
    """Initialize image gallery related session state variables"""
    if 'discogs_images' not in st.session_state:
        st.session_state.discogs_images = []

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
            
        # Create 4 columns for the image grid
        cols = st.columns(3)
        
        # Distribute images across columns
        for idx, image in enumerate(st.session_state.discogs_images):
            col_idx = idx % 3  # Cycle through columns
            
            with cols[col_idx]:
                # Get image dimensions
                try:
                    print(f'Trying to get image from URL: {image["uri"]}')
                    headers = {
                        'User-Agent': 'AlbumCategorizer/1.0'
                    }
                    response = requests.get(image['uri'], headers=headers)
                    print(f'Response status code: {response.status_code}')
                    
                    img = Image.open(BytesIO(response.content))
                    width, height = img.size
                    resolution_text = f' ({width}x{height})'
                    print(f'Successfully got dimensions: {width}x{height}')
                except Exception as e:
                    print(f'Error getting image dimensions: {str(e)}')
                    resolution_text = ''
                
                # Display image with caption and resolution if available
                caption = image.get('type', '').title() + resolution_text
                st.image(
                    image['uri'],
                    caption=caption
                )
        
        st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
