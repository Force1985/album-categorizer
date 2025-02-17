"""
Tag editor component
"""
import streamlit as st
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, COMM
from typing import Optional, Dict, List, Tuple
import math
import base64
from io import BytesIO
import tempfile
import os
from .image_gallery import get_artwork_data

# Define ordered list of common ID3 tags
ORDERED_TAGS = [
    'artwork',        # Album artwork
    'tracknumber',    # Track Number
    'artist',         # Artist
    'title',         # Title
    'length',        # Length
    'genre',         # Genre
    'albumartist',   # Album Artist
    'album',         # Album
    'date',          # Year
    'organization',  # Label
    'copyright',     # Copyright
    'comment',       # Comment
]

# Add comment support to EasyID3
EasyID3.RegisterTextKey('comment', 'COMM:description:eng')

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to MM:SS format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration
    """
    if not seconds or math.isnan(seconds):
        return ''
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

def get_audio_length(uploaded_file) -> str:
    """
    Get audio file length in MM:SS format
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: Audio length in MM:SS format
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        # Write the uploaded file to the temporary file
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.flush()
        
        try:
            # Try as MP3 first
            audio = MP3(tmp_file.name)
            return format_duration(audio.info.length)
        except:
            try:
                # Try generic audio file
                audio = File(tmp_file.name)
                if audio is not None and hasattr(audio.info, 'length'):
                    return format_duration(audio.info.length)
            except:
                pass
        finally:
            # Clean up the temporary file
            try:
                os.unlink(tmp_file.name)
            except:
                pass
                
    return ''

def get_artwork_data_from_file(uploaded_file) -> Optional[bytes]:
    """Get artwork image data from uploaded file"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        # Write the uploaded file to the temporary file
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.flush()
        
        try:
            id3 = ID3(tmp_file.name)
            for tag in id3.getall('APIC'):
                if tag.type == 3:  # Front cover
                    return tag.data
        except:
            pass
        finally:
            # Clean up the temporary file
            try:
                os.unlink(tmp_file.name)
            except:
                pass
    return None

def get_all_id3_tags(uploaded_file) -> Dict[str, str]:
    """
    Get all available ID3 tags from an audio file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Dict[str, str]: Dictionary of all available tags
    """
    tags = {}
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        # Write the uploaded file to the temporary file
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.flush()
        
        try:
            # Try to load as ID3 for standard tags
            audio = EasyID3(tmp_file.name)
            # Get all available tags
            for key in audio.valid_keys.keys():
                value = audio.get(key, [''])[0]
                if value:  # Only include non-empty tags
                    tags[key] = value
                    
            # Load full ID3 tags for artwork and comments
            id3 = ID3(tmp_file.name)
            
            # Try to get artwork
            artwork_data = get_artwork_data_from_file(uploaded_file)
            if artwork_data:
                tags['artwork'] = artwork_data
                
            # Try to get comments
            for tag in id3.getall('COMM'):
                if tag.lang == 'eng':  # Get English comments
                    tags['comment'] = tag.text[0]
                    break
                
        except Exception as e:
            st.error(f"Error reading tags: {str(e)}")
            try:
                # If not ID3, try generic tag support
                audio = File(tmp_file.name, easy=True)
                if audio is not None and hasattr(audio, 'tags'):
                    tags = {key: str(value[0]) for key, value in audio.tags.items() if value}
            except:
                pass
        
        # Try to get length separately
        try:
            length = get_audio_length(uploaded_file)
            if length:
                tags['length'] = length
        except:
            pass
        
        # Clean up the temporary file
        try:
            os.unlink(tmp_file.name)
        except:
            pass
            
    return tags

def edit_tags(uploaded_file, metadata: Dict[str, str]) -> bool:
    """
    Edit ID3 tags of an audio file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        metadata: Dictionary containing tag key-value pairs
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        # Write the uploaded file to the temporary file
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.flush()
        
        try:
            # Load both EasyID3 and full ID3
            audio = EasyID3(tmp_file.name)
            id3 = ID3(tmp_file.name)
            
            # Update standard tags
            for key, value in metadata.items():
                if key not in ['artwork', 'length'] and value:  # Skip artwork and length
                    try:
                        if key == 'comment':
                            # Update comment
                            id3.delall('COMM')  # Remove existing comments
                            id3.add(COMM(
                                encoding=3,
                                lang='eng',
                                desc='description',
                                text=value
                            ))
                        else:
                            # Update other tags
                            audio[key] = value
                    except Exception as e:
                        st.error(f'Error setting {key}: {str(e)}')
                        return False
            
            # Handle artwork separately
            if 'artwork' in metadata and isinstance(metadata['artwork'], bytes):
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
            
            # Save both tag sets
            audio.save()
            id3.save()
            
            # Update the session state with the modified file
            uploaded_file.seek(0)
            with open(tmp_file.name, 'rb') as f:
                uploaded_file.write(f.read())
            
            return True
            
        except Exception as e:
            st.error(f'Error saving tags: {str(e)}')
            return False
        finally:
            # Clean up the temporary file
            try:
                os.unlink(tmp_file.name)
            except:
                pass

def get_tag_display_name(tag_key: str) -> str:
    """
    Convert ID3 tag key to human readable name
    """
    display_names = {
        'artwork': 'Artwork',
        'title': 'Title',
        'artist': 'Artist',
        'album': 'Album',
        'albumartist': 'Album Artist',
        'tracknumber': 'Track Number',
        'discnumber': 'Disc Number',
        'date': 'Year',
        'originaldate': 'Original Year',
        'genre': 'Genre',
        'length': 'Length',
        'composer': 'Composer',
        'conductor': 'Conductor',
        'remixer': 'Remixer',
        'lyricist': 'Lyricist',
        'organization': 'Label',
        'copyright': 'Copyright',
        'comment': 'Comment',
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

def get_ordered_tag_list() -> List[str]:
    """
    Get ordered list of ID3 tags, starting with common tags in specific order,
    followed by remaining tags alphabetically
    """
    # Get all valid tags
    all_tags = set(EasyID3.valid_keys.keys())
    
    # Start with ordered common tags that exist in valid tags
    ordered_tags = [tag for tag in ORDERED_TAGS if tag in all_tags]
    
    # Add remaining tags in alphabetical order
    # remaining_tags = sorted(list(all_tags - set(ordered_tags)))
    
    return ordered_tags# + remaining_tags

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

    # Get current tags from file
    current_tags = get_all_id3_tags(uploaded_file)

    with tags_col1:
        st.markdown("##### Current Tags")
        
        # Show artwork if present
        if 'artwork' in current_tags and isinstance(current_tags['artwork'], bytes):
            st.image(current_tags['artwork'], caption='Current Artwork')
        else:
            st.info('No artwork present')
        
        # Show current tags (read-only)
        for tag_key in get_ordered_tag_list():
            if tag_key not in ['artwork']:  # Skip artwork as it's shown above
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
            # Map track_info fields to ID3 tags
            suggested_tags = {
                'title': track_info.get('title', ''),
                'artist': track_info.get('artist', ''),
                'albumartist': track_info.get('albumartist', ''),
                'album': track_info.get('album', ''),
                'tracknumber': str(track_info.get('position', '')),
                'date': str(track_info.get('year', '')),
                'genre': track_info.get('genre', ''),
                'organization': track_info.get('label', ''),
                'copyright': track_info.get('copyright', ''),
                'comment': track_info.get('comment', '')
            }
        
        # Add file length to suggested tags
        length = get_audio_length(uploaded_file)
        if length:
            suggested_tags['length'] = length
            
        st.markdown("##### Suggested Tags")
        
        # Show selected artwork if available
        if ('discogs_images' in st.session_state and 
            st.session_state.discogs_images and 
            'selected_artwork_index' in st.session_state):
            
            selected_idx = st.session_state.selected_artwork_index
            if 0 <= selected_idx < len(st.session_state.discogs_images):
                selected_image = st.session_state.discogs_images[selected_idx]
                st.image(selected_image['uri'], caption=f'Selected Artwork (Image {selected_idx + 1})')
                
                # Add artwork data to suggested tags
                try:
                    artwork_data = get_artwork_data(selected_image['uri'])
                    suggested_tags['artwork'] = artwork_data
                except Exception as e:
                    st.error(f'Error loading artwork: {str(e)}')
        else:
            st.info('No artwork available from Discogs')
        
        edited_tags = {}
        # Show editable fields with suggestions
        for tag_key in get_ordered_tag_list():
            if tag_key not in ['artwork']:  # Skip artwork as it's shown above
                # Get suggested value, if none available use current value
                suggested_value = suggested_tags.get(tag_key, '')
                
                # Length field should be disabled as it's a file property
                is_disabled = tag_key == 'length'
                
                if tag_key == 'comment':
                    # Use text area for comment
                    edited_value = st.text_input(
                        get_tag_display_name(tag_key),
                        value=suggested_value,
                        key=f'edited_{tag_key}_{id(uploaded_file)}'
                    )
                else:
                    # Use regular text input for other fields
                    edited_value = st.text_input(
                        get_tag_display_name(tag_key),
                        value=suggested_value,
                        disabled=is_disabled,
                        key=f'edited_{tag_key}_{id(uploaded_file)}'
                    )
                
                # Only add to edited_tags if the value is different from current
                if not is_disabled and edited_value and edited_value != current_tags.get(tag_key, ''):
                    edited_tags[tag_key] = edited_value
        
        # Add artwork to edited tags if selected
        if 'artwork' in suggested_tags:
            edited_tags['artwork'] = suggested_tags['artwork']
        
        # Save button
        if edited_tags and st.button('Apply Suggested Tags', key=f'save_tags_{id(uploaded_file)}'):
            if edit_tags(uploaded_file, edited_tags):
                st.success('Tags updated successfully!')
                return edited_tags
    
    return None
