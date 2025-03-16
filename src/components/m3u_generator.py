"""
M3U file generator component
"""
import streamlit as st
from typing import Dict, List
import os

def init_m3u_generator():
    """Initialize M3U generator in session state"""
    if 'm3u_content' not in st.session_state:
        st.session_state.m3u_content = ''

def generate_m3u_content() -> str:
    """
    Generate M3U file content based on track-file pairs
    
    Returns:
        str: M3U file content
    """
    # Get track-file pairs from session state
    track_file_pairs = st.session_state.get('track_file_pairs', {})
    if not track_file_pairs:
        return ''
    
    # Start with the M3U header
    content = '#EXTM3U\n\n'
    
    # Get tracklist from session state
    tracklist = st.session_state.get('tracklist', [])
    if not tracklist:
        return content
    
    # Get uploaded files from session state
    audio_uploader_key = f"audio_files_{st.session_state.get('file_uploader_key', 0)}"
    uploaded_files = st.session_state.get(audio_uploader_key, [])
    
    # Create file options list
    file_options = ["Select file..."] + [f.name for f in uploaded_files]
    
    # Generate M3U entries for each track
    for track_id, file_index in track_file_pairs.items():
        # Skip if track_id is not a valid index
        try:
            track_index = int(track_id)
            if track_index < 0 or track_index >= len(tracklist):
                continue
        except ValueError:
            continue
        
        # Get track information from session state
        position = st.session_state.get(f'track_position_{track_id}', '')
        artist = st.session_state.get(f'track_artist_{track_id}', '')
        title = st.session_state.get(f'track_title_{track_id}', '')
        
        # Get track duration (default to 123 if not available)
        duration = tracklist[track_index].get('duration', '')
        # Convert duration from MM:SS to seconds
        duration_seconds = 123  # Default duration if not available
        if duration:
            try:
                parts = duration.split(':')
                if len(parts) == 2:
                    duration_seconds = int(parts[0]) * 60 + int(parts[1])
            except (ValueError, IndexError):
                pass
        
        # Format track display name - ez az, amit az audio files inputokban látunk
        # Használjuk a track_filename_edits-et, ha elérhető, különben generáljuk a nevet
        if track_id in st.session_state.get('track_filename_edits', {}):
            track_display = st.session_state.track_filename_edits[track_id]
        else:
            track_display = f"{position}. {artist} - {title}"
        
        # Meghatározzuk a fájl kiterjesztését
        file_extension = '.mp3'  # Alapértelmezett kiterjesztés
        
        # Ha van feltöltött fájl ehhez a trackhez, akkor annak a kiterjesztését használjuk
        if file_index > 0 and file_index < len(file_options):
            selected_file = file_options[file_index]
            _, ext = os.path.splitext(selected_file)
            if ext:
                file_extension = ext
        
        # Fájlnév generálása a megfelelő kiterjesztéssel
        filename = f"{track_display}{file_extension}"
        
        # Add EXTINF entry
        content += f'#EXTINF:{duration_seconds}, {track_display}\n'
        content += f'{filename}\n\n'
    
    return content

def save_playlist_file(content: str) -> bool:
    """
    Save the M3U playlist file to the album directory
    
    Args:
        content: M3U file content
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Get folder name from session state
    folder_name = st.session_state.get('combined_output', '')
    if not folder_name:
        st.error('Please set the album folder name first')
        return False
    
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Get export directory
    export_dir = os.path.join(current_dir, 'export', folder_name)

    # Create export directory if it doesn't exist
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Create playlist file path
    playlist_file_path = os.path.join(export_dir, f"{folder_name}.m3u")
    
    # Save the file
    try:
        with open(playlist_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        st.toast(f"Created playlist file: {os.path.basename(playlist_file_path)}", icon="✅")
        return True
    except Exception as e:
        st.toast(f"Error creating playlist file: {str(e)}", icon="❌")
        return False

def render_m3u_generator():
    """Render the M3U generator component"""
    st.subheader("M3U Playlist Generator")
    
    # Initialize session state
    init_m3u_generator()
    
    # Generate M3U content button
    if st.button("Generate M3U Content", type="primary", help="Generate M3U file content based on track-file pairs"):
        # Generáljuk az M3U tartalmat
        st.session_state.m3u_content = generate_m3u_content()
    
    # Display M3U content in a textarea
    m3u_content = st.text_area(
        "M3U Content",
        value=st.session_state.m3u_content,
        height=400,
        help="M3U file content that can be copied and saved as a .m3u file"
    )
    
    # Update session state with any changes made in the textarea
    st.session_state.m3u_content = m3u_content
    
    # Save button - jobbra igazítva, piros gomb
    if m3u_content:
        col1, col2 = st.columns([31, 10])
        with col2:
            if st.button(
                "Save playlist",
                type="primary",
                help="Save the M3U file to the album directory",
                use_container_width=True
            ):
                save_playlist_file(m3u_content)
    
    st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
