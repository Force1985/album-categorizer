import os
import streamlit as st

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
