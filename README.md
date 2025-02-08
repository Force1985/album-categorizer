# Album Categorizer Application

A Streamlit-based web application for organizing and categorizing music albums. The application helps you fetch album information from Discogs and create standardized folder names and info files.

## Features

### Data Input
- Paste a Discogs URL to fetch album information
- All fetched data is displayed in editable fields for customization

### File/Folder Management
- Preview and edit the generated folder name based on album information
- Generate standardized folder names in the format: `Label Catalog# - Artist - Title`
- Preview and edit the info file content
- Save folder structure and info file with standardized formatting

### Album Information
- Display and edit comprehensive album details:
  - Artist and Title
  - Label and Catalog Number
  - Format and Country
  - Release Date and Style
  - Notes
  - Tracklist with support for extra artists

## Installation

1. Create a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To start the application, run:
```bash
streamlit run app.py
```

The application will be available in your browser at: http://localhost:8501

## Usage

1. **Fetch Album Data**:
   - Paste a Discogs URL into the input field
   - Click "Fetch Data" to retrieve album information

2. **Review and Edit Album Information**:
   - All fields are pre-filled with data from Discogs
   - Edit any field as needed to customize the information
   - The tracklist supports adding and editing extra artists

3. **Manage Output**:
   - Preview the generated folder name
   - Use "Edit Preview" to modify the folder name if needed
   - Preview the info file content
   - Use "Edit Preview" to modify the info file content if needed
   - Click "Save Folder" to create the folder structure
   - Click "Save Info File" to save the album information