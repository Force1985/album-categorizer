import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Album Categorizer",
    page_icon="🎵",
    layout="centered"
)

# Main title and description
st.title("Album Categorizer 🎵")
st.write("Fetch and organize your favorite albums from Discogs with ease.")

# Create a row for the input field and button using columns
col1, col2 = st.columns([4, 1], vertical_alignment="bottom")  # 4:1 ratio for input:button

# Input field in the first (wider) column
with col1:
    discogs_url = st.text_input(
        label="Discogs URL",
        placeholder="https://www.discogs.com/release/...",
        help="Paste a Discogs album URL here"
    )

# Button in the second (narrower) column
with col2:
    fetch_button = st.button("Fetch Data", type="primary", use_container_width=True)
