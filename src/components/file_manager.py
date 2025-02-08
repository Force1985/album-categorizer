"""
File manager component
"""
import streamlit as st
from typing import List, Dict

def init_track_file_pairs():
    """Initialize track-file pairs in session state"""
    if 'track_file_pairs' not in st.session_state:
        st.session_state.track_file_pairs = {}
    if 'track_filename_edits' not in st.session_state:
        st.session_state.track_filename_edits = {}
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = 0

def get_track_display(track_id: str) -> str:
    """Get track display text from editable fields"""
    position = st.session_state.get(f'track_position_{track_id}', '')
    artist = st.session_state.get(f'track_artist_{track_id}', '')
    title = st.session_state.get(f'track_title_{track_id}', '')
    
    if artist:
        return f"{position}. {artist} - {title}"
    return f"{position}. {title}"

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
        return

    main_col1, main_sep, main_col2 = st.columns([26, 1, 14])
    
    with main_col1:
        # Get tracklist from session state
        tracklist = st.session_state.get('tracklist', [])
        if not tracklist:
            st.warning("Please fetch release data first to get the tracklist")
            return
        
        # Create matching interface
        st.markdown('##### Match Tracks with Files')
    
        # Create file options list
        file_options = ["Select file..."] + [f.name for f in uploaded_files]
    
        # Create a grid for the matching interface
        for i, track in enumerate(tracklist):
            track_id = str(i)  # track ID az input mezők key-jeihez
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
                elif track_id in st.session_state.track_file_pairs:
                    del st.session_state.track_file_pairs[track_id]
    
    with main_sep:
        st.markdown("<div class='separator-label'> </div>", unsafe_allow_html=True)

    with main_col2:
        # Show matched pairs
        if st.session_state.track_file_pairs:
            st.markdown('##### Matched Pairs')
            
            # Matched pairs list
            for track_id, file_idx in st.session_state.track_file_pairs.items():
                edited_name = st.session_state.track_filename_edits[track_id]
                file_name = file_options[file_idx]
                st.text_input(
                    "Matched Pair",
                    value=f"{edited_name} ← {file_name}",
                    key=f"matched_pair_{track_id}",
                    disabled=True,
                    label_visibility="collapsed"
                )
                
            # Rename Files button
            if st.button(
                "Rename Files",
                type="primary",
                help="Rename files according to the matched tracks",
                use_container_width=True
            ):
                st.info("File renaming will be implemented in the next step")
