"""
File manager component
"""
import streamlit as st
import os
import shutil
import tempfile
from typing import Dict, Optional, List
from ..utils.file_operations import create_album_folder
from .tag_editor import render_tag_editor, edit_tags
from mutagen.id3 import ID3, APIC, COMM
from mutagen.easyid3 import EasyID3

def init_track_file_pairs():
    """Initialize track-file pairs in session state"""
    if 'track_file_pairs' not in st.session_state:
        st.session_state.track_file_pairs = {}
    if 'track_filename_edits' not in st.session_state:
        st.session_state.track_filename_edits = {}
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = 0

def get_track_name(track_id: str) -> str:
    """
    Get the formatted track name from session state
    
    Args:
        track_id: Track ID
        
    Returns:
        str: Formatted track name (e.g. 'A1. Artist - Title')
    """
    position = st.session_state.get(f'track_position_{track_id}', '')
    title = st.session_state.get(f'track_title_{track_id}', '')
    artist = st.session_state.get(f'track_artist_{track_id}', '')
    return f"{position}. {artist} - {title}"

def get_track_display(track_id: str) -> str:
    """Get track display text from editable fields"""
    position = st.session_state.get(f'track_position_{track_id}', '')
    artist = st.session_state.get(f'track_artist_{track_id}', '')
    title = st.session_state.get(f'track_title_{track_id}', '')
    
    if artist:
        return f"{position}. {artist} - {title}"
    return f"{position}. {title}"

def get_track_info(track_id: str) -> dict:
    """Get track information from session state"""
    # Get release date and extract year if available
    release_date = st.session_state.get('info_released', '')
    year = release_date[:4] if release_date and len(release_date) >= 4 else ''
    
    # Get label
    label = st.session_state.get('info_label', '')
    
    # Get album artist from info panel
    album_artist = st.session_state.get('info_artist', '')
    
    # Generate copyright text
    copyright_text = f' {year} {label}' if year and label else ''
    
    # Generate comment text
    notes = st.session_state.get('info_notes', '')
    comment = f'{notes}' if notes else ''
    
    return {
        'position': st.session_state.get(f'track_position_{track_id}', ''),
        'artist': st.session_state.get(f'track_artist_{track_id}', ''),
        'title': st.session_state.get(f'track_title_{track_id}', ''),
        'album': st.session_state.get('info_title', ''),
        'year': year,
        'genre': st.session_state.get('info_style', ''),
        'label': label,
        'copyright': copyright_text,
        'albumartist': album_artist,
        'comment': comment
    }

def get_track_metadata(track_id: str) -> Dict[str, str]:
    """
    Get track metadata from session state
    
    Args:
        track_id: Track ID
        
    Returns:
        Dict[str, str]: Track metadata
    """
    return {
        'tracknumber': st.session_state.get(f'track_position_{track_id}', ''),
        'title': st.session_state.get(f'track_title_{track_id}', ''),
        'artist': st.session_state.get(f'track_artist_{track_id}', ''),
        'album': st.session_state.get('info_title', ''),
        'albumartist': st.session_state.get('info_artist', ''),
        'date': st.session_state.get('info_released', '')[:4] if st.session_state.get('info_released', '') else '',
        'genre': st.session_state.get('info_style', ''),
        'organization': st.session_state.get('info_label', ''),
        'copyright': f"{st.session_state.get('info_released', '')[:4]} {st.session_state.get('info_label', '')}" if st.session_state.get('info_released', '') and st.session_state.get('info_label', '') else '',
        'comment': f"{st.session_state.get('info_notes', '')}" if st.session_state.get('info_notes', '') else '',
        'artwork': st.session_state.get('selected_artwork_data', None)
    }

def create_album_folder(folder_name: str) -> bool:
    """Create album folder"""
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return True
    except Exception as e:
        st.error(f'Error creating album folder: {str(e)}')
        return False

def save_files(uploaded_files: Dict[str, Dict], edited_tags: Dict[str, Dict]) -> bool:
    """
    Save files with edited tags to the export directory
    
    Args:
        uploaded_files: Dictionary of uploaded files with their track matches
        edited_tags: Dictionary of edited tags for each file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get folder name from session state
        folder_name = st.session_state.get('combined_output', '')
        if not folder_name:
            st.error('Please set the album folder name first')
            return False
            
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
            
        # Save each file
        for file_id, file_info in uploaded_files.items():
            if 'file' not in file_info:
                continue
                
            uploaded_file = file_info['file']
            track_id = file_info.get('track_id')
            
            if not track_id:
                continue
                
            # Get track metadata
            metadata = get_track_metadata(track_id)
                
            # Get original file extension
            _, ext = os.path.splitext(uploaded_file.name)
            
            # Get the track name that was matched with this file
            new_filename = get_track_name(track_id) + ext
            
            # Create full path
            export_path = os.path.join(album_dir, new_filename)
            
            # Create a temporary file
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            try:
                # Write the uploaded file to the temporary file
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.close()  # Close the file but don't delete it yet
                
                # Create EasyID3 object for the temporary file
                audio = EasyID3(tmp_file.name)
                
                # Update standard tags
                for key, value in metadata.items():
                    if key not in ['artwork', 'length'] and value:  # Skip artwork and length
                        try:
                            if key == 'comment':
                                # Update comment
                                id3 = ID3(tmp_file.name)
                                id3.delall('COMM')  # Remove existing comments
                                id3.add(COMM(
                                    encoding=3,
                                    lang='eng',
                                    desc='description',
                                    text=value
                                ))
                                id3.save()
                            else:
                                # Update other tags
                                audio[key] = value
                        except Exception as e:
                            st.error(f'Error setting {key}: {str(e)}')
                            return False
                
                # Save standard tags
                audio.save()
                
                # Handle artwork separately
                if 'artwork' in metadata and metadata['artwork']:
                    id3 = ID3(tmp_file.name)
                    # Remove existing artwork
                    id3.delall('APIC')
                    # Add new artwork
                    id3.add(APIC(
                        encoding=3,  # UTF-8
                        mime='image/jpeg',  # Image MIME type
                        type=3,  # Cover (front)
                        desc='Cover',
                        data=metadata['artwork']
                    ))
                    id3.save()
                
                # Copy the file with updated tags to the export directory
                shutil.copy2(tmp_file.name, export_path)
                
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
                    
        st.success(f'Successfully saved files to {folder_name}')
        return True
        
    except Exception as e:
        st.error(f'Error saving files: {str(e)}')
        return False

def render_file_manager():
    """Render the file manager component"""
    st.subheader("Audio Files")
    
    # Initialize session state
    init_track_file_pairs()

    # File uploader with dynamic key
    uploaded_files = st.file_uploader(
        "Drop audio files here",
        accept_multiple_files=True,
        type=['mp3', 'flac', 'wav', 'm4a', 'aac'],
        key=f"audio_files_{st.session_state.file_uploader_key}"
    )

    if not uploaded_files:
        st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
        return

    # Get tracklist from session state
    tracklist = st.session_state.get('tracklist', [])
    if not tracklist:
        st.warning("Please fetch release data first to get the tracklist")
        return
    
    # Create file options list
    file_options = ["Select file..."] + [f.name for f in uploaded_files]
    
    # Create matching interface
    st.markdown('##### Match Tracks with Files')
    
    # Create a grid for the matching interface
    edited_tags = {}
    for i, track in enumerate(tracklist):
        track_id = str(i)
        
        # Track row with two columns
        col1, sep, col2 = st.columns([10, 1, 10])
        
        with col1:
            # Track display szöveg generálása
            track_display = get_track_display(track_id)
            
            # If there is no edited name, initialize it
            if track_id not in st.session_state.track_filename_edits:
                st.session_state.track_filename_edits[track_id] = track_display
            
            # Track name input
            edited_name = st.text_input(
                "Track Name",
                value=st.session_state.track_filename_edits[track_id],
                key=f"track_filename_{track_id}",
                label_visibility="collapsed"
            )
            # Store edited name in session state
            st.session_state.track_filename_edits[track_id] = edited_name
            
        with sep:
            st.markdown("<div class='separator-nolabel'>←</div>", unsafe_allow_html=True)
            
        with col2:
            # File selection
            selected_file = st.selectbox(
                "File",
                options=file_options,
                index=st.session_state.track_file_pairs.get(track_id, 0),
                key=f"file_select_{i}",
                label_visibility="collapsed"
            )
            
            # Store selection in session state
            if selected_file != "Select file...":
                # Remove this file from other tracks if it was selected elsewhere
                for pos in list(st.session_state.track_file_pairs.keys()):
                    if (pos != track_id and 
                        file_options[st.session_state.track_file_pairs[pos]] == selected_file):
                        del st.session_state.track_file_pairs[pos]
                
                st.session_state.track_file_pairs[track_id] = file_options.index(selected_file)
                
                # Get the actual file object for the selected file
                selected_file_obj = next(
                    (f for f in uploaded_files if f.name == selected_file),
                    None
                )
                
                # Get track info for suggestions
                track_info = get_track_info(track_id)
                
            elif track_id in st.session_state.track_file_pairs:
                del st.session_state.track_file_pairs[track_id]
        
        # Show tag editor for the selected file with track info
        if selected_file != "Select file..." and selected_file_obj:
            with st.expander(f"Edit Tags for Track {i + 1}: {edited_name}", expanded=False):
                edited_tags[track_id] = render_tag_editor(selected_file_obj, track_info)

    col3, col4 = st.columns([31, 10])
    
    with col4:
        # Save Files button
        if st.button(
            "Save Files",
            type="primary",
            help="Save files to the export directory",
            use_container_width=True
        ):
            save_files({str(i): {'file': f, 'track_id': str(i)} for i, f in enumerate(uploaded_files)}, edited_tags)

    st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
