"""
Tag editor component
"""
import streamlit as st
from mutagen import File
from mutagen.easyid3 import EasyID3
from typing import Optional, Dict, List, Tuple

def get_all_id3_tags(file) -> Dict[str, str]:
    """
    Get all available ID3 tags from an audio file
    
    Args:
        file: Audio file object
        
    Returns:
        Dict[str, str]: Dictionary of all available tags
    """
    try:
        audio = EasyID3(file)
        # Get all available tags
        tags = {}
        for key in audio.valid_keys.keys():
            value = audio.get(key, [''])[0]
            if value:  # Only include non-empty tags
                tags[key] = value
        return tags
    except:
        try:
            # If not ID3, try generic tag support
            audio = File(file, easy=True)
            if audio is not None:
                return {key: str(value[0]) for key, value in audio.tags.items() if value}
        except:
            pass
    return {}

def edit_tags(file, metadata: Dict[str, str]) -> bool:
    """
    Edit ID3 tags of an audio file
    
    Args:
        file: Audio file object
        metadata: Dictionary containing tag key-value pairs
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Try to load as ID3
        audio = EasyID3(file)
    except:
        try:
            # If not ID3, try generic tag support
            audio = File(file, easy=True)
        except:
            st.error(f'Could not load tags for file: {file}')
            return False
    
    if audio is None:
        st.error(f'File format not supported: {file}')
        return False
        
    # Update tags
    for key, value in metadata.items():
        if value:  # Only set non-empty values
            try:
                audio[key] = value
            except Exception as e:
                st.error(f'Error setting {key}: {str(e)}')
                return False
    
    # Save changes
    try:
        audio.save()
        return True
    except Exception as e:
        st.error(f'Error saving tags: {str(e)}')
        return False

def get_tag_display_name(tag_key: str) -> str:
    """
    Convert ID3 tag key to human readable name
    """
    display_names = {
        'title': 'Title',
        'artist': 'Artist',
        'album': 'Album',
        'albumartist': 'Album Artist',
        'tracknumber': 'Track Number',
        'discnumber': 'Disc Number',
        'date': 'Year',
        'originaldate': 'Original Year',
        'genre': 'Genre',
        'composer': 'Composer',
        'conductor': 'Conductor',
        'remixer': 'Remixer',
        'lyricist': 'Lyricist',
        'organization': 'Label',
        'copyright': 'Copyright',
        'encodedby': 'Encoded By',
        'bpm': 'BPM',
        'compilation': 'Part of Compilation',
        'language': 'Language',
        'isrc': 'ISRC',
        'barcode': 'Barcode',
        'catalognumber': 'Catalog Number',
        'media': 'Media Type',
        'mood': 'Mood',
        'version': 'Version',
        'website': 'Website'
    }
    return display_names.get(tag_key, tag_key.title())

def render_tag_editor(uploaded_file, track_info: Optional[Dict] = None) -> Optional[Dict[str, str]]:
    """
    Render tag editor interface for an audio file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        track_info: Optional dictionary containing suggested track information
        
    Returns:
        Optional[Dict[str, str]]: Dictionary of edited tags if save was clicked
    """
    if not uploaded_file:
        return None
    
    tags_col1, tags_sep, tags_col2 = st.columns([20, 1, 20])

    with tags_col1:
        # Get current tags
        current_tags = get_all_id3_tags(uploaded_file)

        # Create two columns for current and suggested tags
        st.markdown("##### Current Tags")
        for tag_key in EasyID3.valid_keys.keys():
            current_value = current_tags.get(tag_key, '')
            st.text_input(
                get_tag_display_name(tag_key),
                value=current_value,
                disabled=True,
                key=f'current_{tag_key}_{id(uploaded_file)}'
            )

    with tags_sep:
        st.markdown("<div class='separator'> </div>", unsafe_allow_html=True)
    
    with tags_col2:
        # Create suggested tags from track_info if available
        suggested_tags = {}
        if track_info:
            # Map track_info fields to ID3 tags - this mapping should be customized
            # based on your track_info structure
            suggested_tags = {
                'title': track_info.get('title', ''),
                'artist': track_info.get('artist', ''),
                'album': track_info.get('album', ''),
                'tracknumber': str(track_info.get('position', '')),
                'date': str(track_info.get('year', '')),
                'genre': track_info.get('genre', ''),
                'organization': track_info.get('label', ''),
                # Add more mappings as needed
            }
            
        # Show editable fields with suggestions
        st.markdown("##### Suggested Tags")
        edited_tags = {}
        for tag_key in EasyID3.valid_keys.keys():
            suggested_value = suggested_tags.get(tag_key, '')
            edited_value = st.text_input(
                get_tag_display_name(tag_key),
                value=suggested_value,
                key=f'edited_{tag_key}_{id(uploaded_file)}'
            )
            if edited_value and edited_value != current_tags.get(tag_key, ''):
                edited_tags[tag_key] = edited_value
        
        # Save button
        if edited_tags and st.button('Apply Suggested Tags', key=f'save_tags_{id(uploaded_file)}'):
            if edit_tags(uploaded_file, edited_tags):
                st.success('Tags updated successfully!')
                return edited_tags
    
    return None
