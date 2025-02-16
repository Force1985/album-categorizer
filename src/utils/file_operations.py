"""
File operations utilities
"""
import os
import streamlit as st
import requests
from io import BytesIO
from PIL import Image

def create_album_folder(folder_name):
    """Create a folder for the album in the export directory"""
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Create export directory if it doesn't exist
    export_dir = os.path.join(current_dir, 'export')
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Create the album directory inside export
    album_dir = os.path.join(export_dir, folder_name)
    if not os.path.exists(album_dir):
        os.makedirs(album_dir)
        st.toast(f"Created folder: {os.path.basename(album_dir)}", icon="✅")
        return True
    else:
        st.toast(f"Folder already exists: {os.path.basename(album_dir)}", icon="⚠️")
        return False

def create_info_file(folder_name, content):
    """Create an info file for the album in the export directory"""
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Get export directory
    export_dir = os.path.join(current_dir, 'export', folder_name)

    # Create export directory if it doesn't exist
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Create info file path
    info_file_path = os.path.join(export_dir, f"{folder_name}.txt")
    
    # Check if the file already exists
    try:
        with open(info_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        st.toast(f"Created info file: {os.path.basename(info_file_path)}", icon="✅")
        return True
    except Exception as e:
        st.toast(f"Error creating info file: {str(e)}", icon="❌")
        return False

def save_image(image_url, folder_name, image_type):
    """Create an image file for the album in the export directory"""
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Get export directory
    export_dir = os.path.join(current_dir, 'export', folder_name)

    # Create export directory if it doesn't exist
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    try:
        # Download image
        headers = {
            'User-Agent': 'AlbumCategorizer/1.0'
        }
        response = requests.get(image_url, headers=headers)
        if response.status_code != 200:
            st.toast(f"Failed to download image: HTTP {response.status_code}", icon="❌")
            return False

        # Create filename with type suffix
        filename = f"{folder_name} ({image_type}).jpg"
        file_path = os.path.join(export_dir, filename)
        
        # Save image
        with open(file_path, 'wb') as f:
            f.write(response.content)
        st.toast(f"Saved image: {os.path.basename(file_path)}", icon="✅")
        return True
    except Exception as e:
        st.toast(f"Error saving image: {str(e)}", icon="❌")
        return False
