"""
Settings Modal Component
"""
import streamlit as st
from typing import Tuple
import os
from dotenv import load_dotenv

def init_settings():
    """Initialize settings related session state variables and load from .env"""
    # Initialize session state variables if not exist
    if 'discogs_token' not in st.session_state:
        st.session_state.discogs_token = ''
    
    # Load from .env if exists
    load_dotenv()
    
    if os.getenv('DISCOGS_TOKEN'):
        st.session_state.discogs_token = os.getenv('DISCOGS_TOKEN')

def render_settings() -> None:
    """Render the settings popover"""
    with st.popover('⚙️ Settings', use_container_width=True):
        # Discogs API section
        st.markdown('#### 💿 Discogs API')
        st.markdown("""
        To get your Discogs API token:
        1. Go to [Discogs Developer Settings](https://www.discogs.com/settings/developers)
        2. Generate a new token
        3. Copy and paste it below
        """)
        
        discogs_token = st.text_input(
            'Discogs Token',
            value=st.session_state.discogs_token,
            type='password',
            key='settings_discogs_token_input'
        )
        st.session_state.discogs_token = discogs_token
        
        st.markdown('---')
        st.markdown("""
        💡 **Tip**: You can also set these values in a `.env` file:
        ```
        DISCOGS_TOKEN=your_token
        ```
        """)
