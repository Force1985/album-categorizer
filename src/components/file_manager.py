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
import requests
import re

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

def get_track_info(track_id: str) -> Dict[str, str]:
    """
    Get track information from session state
    
    Args:
        track_id: Track ID
        
    Returns:
        Dict containing track information including artist, album, title,
        position (original string), tracknumber (numeric part) and 
        discnumber (A/B/C/D converted to 1/2/3/4)
    """
    # Get release date and extract year if available
    release_date = st.session_state.get('info_released', '')
    year = release_date[:4] if release_date and len(release_date) >= 4 else ''
    
    # Get label
    label = st.session_state.get('info_label', '')
    
    # Get album artist from info panel
    album_artist = st.session_state.get('info_artist', '')
    
    # Generate copyright text
    copyright_text = f'{year} {label}' if year and label else ''
    
    # Get credit line for comment
    comment = st.session_state.get('info_credit_line', '')
    
    # Get position and split into disc (A/B) and track number
    position = st.session_state.get(f'track_position_{track_id}', '')
    disc_number = '1'  # Default to disc 1
    track_number = ''
    
    if position:
        # Extract A/B and number from position (e.g., "A1", "B2")
        if position.upper().startswith('A'):
            disc_number = '1'
            track_number = position[1:]
        elif position.upper().startswith('B'):
            disc_number = '2'
            track_number = position[1:]
        elif position.upper().startswith('C'):
            disc_number = '3'
            track_number = position[1:]
        elif position.upper().startswith('D'):
            disc_number = '4'
            track_number = position[1:]
        else:
            # If no letter prefix, just use the number
            track_number = position
    
    # Extract only numbers from track_number
    track_number = ''.join(re.findall(r'\d+', track_number)) if track_number else ''
    
    return {
        'position': position,  # Keep original position for display
        'artist': st.session_state.get(f'track_artist_{track_id}', ''),
        'title': st.session_state.get(f'track_title_{track_id}', ''),
        'album': st.session_state.get('info_title', ''),
        'year': year,
        'genre': st.session_state.get('info_style', ''),
        'label': label,
        'copyright': copyright_text,
        'albumartist': album_artist,
        'comment': comment,
        'tracknumber': track_number,
        'discnumber': disc_number
    }

def get_track_metadata(track_id: str) -> Dict[str, str]:
    """
    Get track metadata from session state
    
    Args:
        track_id: Track ID
        
    Returns:
        Dict[str, str]: Track metadata
    """
    # Get artwork data
    artwork_data = None
    if 'selected_artwork' in st.session_state:
        artwork_url = st.session_state.selected_artwork
        try:
            # Download artwork data with proper headers
            headers = {
                'User-Agent': 'AlbumCategorizer/1.0',
                'Referer': 'https://www.discogs.com/'
            }
            response = requests.get(artwork_url, headers=headers)
            if response.status_code == 200:
                artwork_data = response.content
                # st.write("Debug - Downloaded artwork data length:", len(artwork_data))
            else:
                st.error(f"Error downloading artwork: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error downloading artwork: {str(e)}")
    
    # Get track info
    track_info = get_track_info(track_id)
    
    metadata = {
        'discnumber': track_info['discnumber'],
        'tracknumber': track_info['tracknumber'],
        'title': track_info['title'],
        'artist': track_info['artist'],
        'album': track_info['album'],
        'albumartist': track_info['albumartist'],
        'date': track_info['year'],
        'genre': track_info['genre'],
        'organization': track_info['label'],
        'copyright': track_info['copyright'],
        'comment': track_info['comment'],
        'artwork': artwork_data
    }
    
    # Debug log
    # st.write("Debug - Metadata:", {k: str(v)[:100] + '...' if isinstance(v, bytes) else v for k, v in metadata.items()})
    # st.write("Debug - Session state keys:", list(st.session_state.keys()))
    # st.write("Debug - Selected artwork URL:", st.session_state.get('selected_artwork', 'Not found'))
    
    return metadata

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
                
                if ext == '.flac':
                    from mutagen.flac import FLAC, Picture
                    # Load FLAC file
                    audio = FLAC(tmp_file.name)
                    
                    # Clear existing tags and pictures
                    audio.clear_pictures()
                    audio.tags.clear()
                    
                    # Add new tags
                    for key, value in metadata.items():
                        if key == 'artwork' and isinstance(value, bytes):
                            picture = Picture()
                            picture.type = 3  # Front cover
                            picture.mime = 'image/jpeg'
                            picture.desc = 'Front cover'
                            picture.data = value
                            audio.add_picture(picture)
                        elif key not in ['artwork', 'length']:
                            # Convert keys to FLAC standard
                            flac_key = {
                                'tracknumber': 'TRACKNUMBER',
                                'discnumber': 'DISCNUMBER',
                                'albumartist': 'ALBUMARTIST',
                                'genre': 'GENRE',
                                'artist': 'ARTIST',
                                'title': 'TITLE',
                                'album': 'ALBUM',
                                'date': 'DATE',
                                'organization': 'ORGANIZATION',
                                'copyright': 'COPYRIGHT',
                                'comment': 'DESCRIPTION'
                            }.get(key.lower(), key.upper())
                            
                            if value:  # Only add non-empty values
                                audio.tags[flac_key] = str(value)
                    
                    # Save changes
                    audio.save()
                else:
                    try:
                        # First try to delete all existing ID3 tags
                        id3 = ID3(tmp_file.name)
                        id3.delete()
                        id3.save()
                    except:
                        # If the file doesn't have ID3 tags yet, create them
                        try:
                            id3 = ID3()
                            id3.save(tmp_file.name)
                        except Exception as e:
                            st.error(f'Error initializing ID3 tags: {str(e)}')
                            return False
                    
                    try:
                        # Initialize EasyID3
                        audio = EasyID3(tmp_file.name)
                    except:
                        # If EasyID3 tags don't exist, add them
                        try:
                            EasyID3.create(tmp_file.name)
                            audio = EasyID3(tmp_file.name)
                        except Exception as e:
                            st.error(f'Error initializing EasyID3 tags: {str(e)}')
                            return False
                    
                    # Update standard tags first
                    for key, value in metadata.items():
                        if key not in ['artwork', 'length', 'comment'] and value:  # Skip artwork, length and comment
                            try:
                                audio[key] = value
                            except Exception as e:
                                st.error(f'Error setting {key}: {str(e)}')
                                return False
                    
                    # Save standard tags
                    audio.save()
                    
                    # Now handle comment and artwork with full ID3
                    id3 = ID3(tmp_file.name)
                    
                    # Add comment if present
                    if metadata.get('comment'):
                        # Remove existing comments
                        id3.delall('COMM')
                        # Add new comment
                        id3.add(COMM(
                            encoding=3,
                            lang='eng',
                            desc='description',
                            text=metadata['comment']
                        ))
                        # st.write("Debug - Added comment:", metadata['comment'])
                    
                    # Add artwork if present
                    if metadata.get('artwork'):
                        # st.write("Debug - Adding artwork...")
                        try:
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
                            # st.write("Debug - Successfully added artwork")
                        except Exception as e:
                            st.error(f"Error adding artwork: {str(e)}")
                    
                    # Save ID3 tags
                    try:
                        id3.save(v2_version=3)
                        # st.write("Debug - Saved ID3 tags")
                    except Exception as e:
                        st.error(f"Error saving ID3 tags: {str(e)}")
                
                # Copy the file with updated tags to the export directory
                shutil.copy2(tmp_file.name, export_path)
                
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
                    
        st.toast(f"Successfully saved files to {folder_name}", icon="✅")
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
