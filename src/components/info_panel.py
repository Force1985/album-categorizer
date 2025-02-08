"""
Info panel component
"""
import streamlit as st
from ..transformations.info import (
    transform_info_artist,
    transform_info_label,
    transform_info_format,
    transform_info_notes,
    transform_info_url,
    transform_info_tracklist
)
from ..utils.file_operations import create_info_file

def render_track_editor(track: dict, index: int) -> dict:
    """
    Render editor for a single track
    
    Args:
        track: Track data
        index: Track index for unique keys
        
    Returns:
        Updated track data
    """

    # Main grid
    cols = st.columns([2, 4, 8, 2])
    
    with cols[0]:
        # Position input
        position = st.text_input(
            'Position',
            value=track.get('position', ''),
            key=f'track_position_{index}'
        )
    
    with cols[1]:
        # Artist input
        artist = st.text_input(
            'Artist',
            value=track.get('artist', ''),
            key=f'track_artist_{index}'
        )
    
    with cols[2]:
        # Title input
        title = st.text_input(
            'Title',
            value=track.get('title', ''),
            key=f'track_title_{index}'
        )
    
    with cols[3]:
        # Duration input
        duration = st.text_input(
            'Duration',
            value=track.get('duration', ''),
            key=f'track_duration_{index}'
        )
    
    # Extra artists expander
    with st.expander('Extra Artists', expanded=False):
        extra_artists = track.get('extra_artists', [])
        updated_extra_artists = []
        
        # Add new extra artist button
        if st.button('Add Extra Artist', key=f'add_extra_{index}'):
            extra_artists.append({'role': '', 'name': ''})
        
        # Edit existing extra artists
        for i, extra in enumerate(extra_artists):
            cols = st.columns([1, 1])
            with cols[0]:
                # Role input
                role = st.text_input(
                    'Role',
                    value=extra.get('role', ''),
                    key=f'extra_role_{index}_{i}'
                )
            with cols[1]:
                # Name input
                name = st.text_input(
                    'Name',
                    value=extra.get('name', ''),
                    key=f'extra_name_{index}_{i}'
                )
            
            if role or name:  # Only add if either field has content
                updated_extra_artists.append({
                    'role': role,
                    'name': name
                })
    
    return {
        'position': position,
        'artist': artist,
        'title': title,
        'duration': duration,
        'extra_artists': updated_extra_artists
    }

def render_info_panel():
    """
    Renders the information panel component that displays album and collection details.
    """
    with st.container():
        st.subheader('Album Information')

        # Main grid
        main_col1, main_sep, main_col2 = st.columns([20, 1, 20])

        with main_col1:
            # First row
            col1, col2 = st.columns([10, 10])

            with col1:
                # Artist input
                info_artist = st.text_input(
                    f"Artist / API: {st.session_state.original_artists_sort}" if 'original_artists_sort' in st.session_state else "Artist",
                    value=transform_info_artist(st.session_state.get('original_artists_sort', '')),
                    key="info_artist"
                )

            with col2:
                # Title input
                info_title = st.text_input(
                    f"Title / API: {st.session_state.original_title}" if 'original_title' in st.session_state else "Title",
                    value=st.session_state.get('original_title', ''),
                    key="info_title"
                )

            # Second row
            col1, col2 = st.columns([10, 10])

            with col1:
                # Label input
                info_label = st.text_input(
                    f"Label / API: {st.session_state.original_label}" if 'original_label' in st.session_state else "Label",
                    value=transform_info_label(st.session_state.get('original_label', '')),
                    key="info_label"
                )
            with col2:
                # Catalog number input
                info_catalog = st.text_input(
                    f"Catalog# / API: {st.session_state.original_catalog}" if 'original_catalog' in st.session_state else "Catalog#",
                    value=st.session_state.get('original_catalog', ''),
                    key="info_catalog"
                )

            # Third row
            col1, col2 = st.columns([10, 10])

            with col1:
                # Build format label parts
                format_label_parts = []
                if 'original_formats_qty' in st.session_state and st.session_state.original_formats_qty:
                    format_label_parts.append(f"q: {st.session_state.original_formats_qty}")
                if 'original_formats_name' in st.session_state and st.session_state.original_formats_name:
                    format_label_parts.append(f"n: {st.session_state.original_formats_name}")
                if 'original_format_descriptions' in st.session_state and st.session_state.original_format_descriptions:
                    format_label_parts.append(f"d: {st.session_state.original_format_descriptions}")
                if 'original_format_text' in st.session_state and st.session_state.original_format_text:
                    format_label_parts.append(f"t: {st.session_state.original_format_text}")
                    
                format_label = "Format / API: " + ", ".join(format_label_parts) if format_label_parts else "Format"
                
                formatted_format = transform_info_format(
                    st.session_state.get('formats_qty', ''),
                    st.session_state.get('formats_name', ''),
                    st.session_state.get('format_descriptions', []),
                    st.session_state.get('format_text', '')
                )

                # Format input
                info_format = st.text_input(
                    format_label,
                    value=formatted_format,
                    key="info_format"
                )

            with col2:
                # Country input
                info_country = st.text_input(
                    f"Country / API: {st.session_state.original_country}" if 'original_country' in st.session_state else "Country",
                    value=st.session_state.get('original_country', ''),
                    key="info_country"
                )
            
            # Fourth row
            col7, col8 = st.columns([10, 10])
            
            with col7:
                # Released input
                info_released = st.text_input(
                    f"Released / API: {st.session_state.original_released}" if 'original_released' in st.session_state else "Released",
                    value=st.session_state.get('original_released', ''),
                    key="info_released"
                )

            with col8:
                # Style input
                info_style = st.text_input(
                    f"Style / API: {st.session_state.original_style}" if 'original_style' in st.session_state else "Style",
                    value=st.session_state.get('original_style', ''),
                    key="info_style"
                )
            
            # Notes input
            notes_label = st.session_state.get('original_notes', '')
            info_notes = st.text_area(
                f"Notes / API: {notes_label}" if notes_label else "Notes",
                value=transform_info_notes(
                    st.session_state.get('original_notes', ''),
                    st.session_state.get('original_artists_sort', ''),
                    st.session_state.get('original_format_descriptions', []),
                    st.session_state.get('api_response', {})
                ),
                key='info_notes',
                height=202
            )

            # Tracklist
            st.markdown('#### Tracklist')
            
            # Initialize or update tracklist in session state
            api_response = st.session_state.get('api_response', {})
            if 'tracklist' not in st.session_state or api_response != st.session_state.get('last_api_response'):
                tracklist_data = transform_info_tracklist(
                    api_response.get('tracklist', []),
                    st.session_state.get('info_artist', '')  # Pass the album artist
                )
                st.session_state.tracklist = tracklist_data
                st.session_state.last_api_response = api_response
                
            # Add new track button
            if st.button('Add Track'):
                next_position = len(st.session_state.tracklist) + 1
                st.session_state.tracklist.append({
                    'position': f"{next_position:02d}",
                    'artist': '',
                    'title': '',
                    'duration': '',
                    'extra_artists': []
                })
            
            # Edit existing tracks
            updated_tracklist = []
            for i, track in enumerate(st.session_state.tracklist):
                with st.container():
                    # st.markdown(f'###### Track {i+1}')
                    updated_track = render_track_editor(track, i)
                    updated_tracklist.append(updated_track)
            
            # Update session state
            st.session_state.tracklist = updated_tracklist

        with main_sep:
            st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
        
        with main_col2:
            # Format multi-line notes with proper indentation
            notes_content = st.session_state.info_notes.split('\n')
            formatted_notes = 'Notes:     ' + notes_content[0]
            if len(notes_content) > 1:
                formatted_notes += '\n' + '\n'.join('           ' + line for line in notes_content[1:])

            # Display the template
            info_file_template = f"""{st.session_state.info_artist} - {st.session_state.info_title}

Label:     {st.session_state.info_label}
Catalog#:  {st.session_state.info_catalog}
Format:    {st.session_state.info_format}
Country:   {st.session_state.info_country}
Released:  {st.session_state.info_released}
Style:     {st.session_state.info_style}
Discogs:   {transform_info_url(st.session_state.discogs_url)}
{formatted_notes}

Tracklist:"""

            # Calculate the length of the longest title line
            max_line_length = 0
            for track in st.session_state.tracklist:
                line_length = len(f"{track['position']}. ")
                if track['artist']:
                    line_length += len(track['artist']) + 3  # +3 for " - "
                line_length += len(track['title'])
                max_line_length = max(max_line_length, line_length)
            
            # Add 4 spaces padding after the longest line
            duration_position = max_line_length + 4

            # Add tracks to template
            for track in st.session_state.tracklist:
                # Start with position and title
                line = f"\n{track['position']}. "
                if track['artist']:
                    line += f"{track['artist']} - "
                line += track['title']
                
                # Add padding to align duration
                if track['duration']:
                    current_length = len(line)
                    padding = " " * (duration_position - current_length)
                    line += f"{padding}{track['duration']}"
                
                info_file_template += line
                
                # Add extra artists
                for extra in track['extra_artists']:
                    if extra['role'] and extra['name']:
                        info_file_template += f"\n    {extra['role']} - {extra['name']}"

            # Preview section
            st.text_area(
                label="Preview",
                value=info_file_template,
                height=450,
                disabled=st.session_state.get('info_preview_disabled', True),
                key="preview-text",
                help="Preview of the info file"
            )

            st.markdown("<div class='separator-label separator-label--sm'> </div>", unsafe_allow_html=True)
        
            col1, col2 = st.columns([1, 1])

            with col1:
                # Show preview in a sticky element
                st.markdown("<div class='sticky-preview'> </div>", unsafe_allow_html=True)

                # Edit preview button
                if st.button(
                    "Edit Preview",
                    key="edit_info_preview_btn",
                    type="secondary",
                    help="Enable editing of the preview",
                    use_container_width=True
                ):
                    st.session_state.info_preview_disabled = False
                    st.rerun()
                    
            with col2:
                # Show preview in a sticky element
                st.markdown("<div class='sticky-preview'> </div>", unsafe_allow_html=True)

                # Save info file button
                if st.button(
                    "Save Info File",
                    key="save_info_btn",
                    type="primary",
                    help="Save a text file with the album info",
                    use_container_width=True
                ): 
                    # Get folder name from session state
                    folder_name = f"{st.session_state.label} {st.session_state.catalog} - {st.session_state.artist} - {st.session_state.title}"
                    create_info_file(folder_name, info_file_template)
    
    st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
