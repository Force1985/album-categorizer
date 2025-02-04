import streamlit as st

def render_info_panel():
    """
    Renders the information panel component that displays album and collection details.
    """
    with st.container():
        st.subheader('Album Information')
        
        template = """[artists_sort] - [title]

Label: [labels.name]
Catalog#: [labels.catno]
Format: [formats.qty]x[formats.name], [formats.descriptions]
Country: [country]
Released: [released]
Style: [styles]
Notes: Written & produced by ???.
[notes]
Discogs: [uri]

Tracklist:
[tracklist.position]. [artists_sort] - [tracklist.title]    [tracklist.duration]
    [extraartists.role] - [extraartists.name]"""

        st.text_area(
            label="Info Template",
            value=template,
            height=400,
            disabled=True
        )
