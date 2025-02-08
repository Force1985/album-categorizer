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

def render_track_editor(track: dict, index: int) -> dict:
    """
    Render editor for a single track
    
    Args:
        track: Track data
        index: Track index for unique keys
        
    Returns:
        Updated track data
    """
    cols = st.columns([2, 3, 8, 3])
    
    with cols[0]:
        position = st.text_input(
            'Position',
            value=track.get('position', ''),
            key=f'track_position_{index}'
        )
    
    with cols[1]:
        artist = st.text_input(
            'Artist',
            value=track.get('artist', ''),
            key=f'track_artist_{index}'
        )
    
    with cols[2]:
        title = st.text_input(
            'Title',
            value=track.get('title', ''),
            key=f'track_title_{index}'
        )
    
    with cols[3]:
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
                role = st.text_input(
                    'Role',
                    value=extra.get('role', ''),
                    key=f'extra_role_{index}_{i}'
                )
            with cols[1]:
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

        # Main grid - 3 columns (21-1-21)
        main_col1, main_sep, main_col2 = st.columns([21, 1, 21])

        with main_col1:
            # First row in the nested grid
            col1, sep1, col2 = st.columns([10, 1, 10])

            with col1:
                info_artist = st.text_input(
                    f"Artist / API: {st.session_state.original_artists_sort}" if 'original_artists_sort' in st.session_state else "Artist",
                    value=transform_info_artist(st.session_state.get('original_artists_sort', '')),
                    key="info_artist"
                )
            with sep1:
                st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
            with col2:
                info_title = st.text_input(
                    f"Title / API: {st.session_state.original_title}" if 'original_title' in st.session_state else "Title",
                    value=st.session_state.get('original_title', ''),
                    key="info_title"
                )

            # Second row
            col1, sep1, col2 = st.columns([10, 1, 10])

            with col1:
                info_label = st.text_input(
                    f"Label / API: {st.session_state.original_label}" if 'original_label' in st.session_state else "Label",
                    value=transform_info_label(st.session_state.get('original_label', '')),
                    key="info_label"
                )
            with sep1:
                st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
            with col2:
                info_catalog = st.text_input(
                    f"Catalog# / API: {st.session_state.original_catalog}" if 'original_catalog' in st.session_state else "Catalog#",
                    value=st.session_state.get('original_catalog', ''),
                    key="info_catalog"
                )

            # Third row
            col1, sep1, col2 = st.columns([10, 1, 10])

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
                info_format = st.text_input(
                    format_label,
                    value=formatted_format,
                    key="info_format"
                )
            with sep1:
                st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
            with col2:
                info_country = st.text_input(
                    f"Country / API: {st.session_state.original_country}" if 'original_country' in st.session_state else "Country",
                    value=st.session_state.get('original_country', ''),
                    key="info_country"
                )
            
            # Fourth row in the nested grid
            col7, sep4, col8 = st.columns([10, 1, 10])
            
            with col7:
                info_released = st.text_input(
                    f"Released / API: {st.session_state.original_released}" if 'original_released' in st.session_state else "Released",
                    value=st.session_state.get('original_released', ''),
                    key="info_released"
                )
            with sep4:
                st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
            with col8:
                info_style = st.text_input(
                    f"Style / API: {st.session_state.original_style}" if 'original_style' in st.session_state else "Style",
                    value=st.session_state.get('original_style', ''),
                    key="info_style"
                )
            
            # Notes
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
                height=198
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

            st.text_area(
                label="Preview",
                value=info_file_template,
                height=450,
                disabled=st.session_state.get('info_preview_disabled', True),
                key="preview-text",
                help="Preview of the info file"
            )

            st.markdown("<div class='separator-label'> </div>", unsafe_allow_html=True)
        
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(
                    "Edit Info",
                    key="edit_info_btn",
                    type="secondary",
                    help="Enable editing of the preview",
                    use_container_width=True
                ):
                    st.session_state.info_preview_disabled = False
                    st.rerun()
                    
            with col2:
                if st.button(
                    "Save Info File",
                    key="save_info_btn",
                    type="primary",
                    help="Save a text file with the album info",
                    use_container_width=True
                ): 
                    # create_info_file(info_file_template)
                    pass

            # Show preview in a sticky element
            main_col2.write("""<div class='sticky-preview' />""", unsafe_allow_html=True)
    
    st.markdown("<div class='separator-line'> </div>", unsafe_allow_html=True)
