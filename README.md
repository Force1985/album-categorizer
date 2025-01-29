# Album Categorizer

An application to categorize and manage your music album collection using Discogs API.

## Features

- Search and fetch album information from Discogs
- Categorize albums based on various criteria
- Modern React frontend with Bootstrap
- Python backend API

## Project Structure

```
album-categorizer/
├── backend/           # Python Flask backend
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # React frontend
│   ├── public/
│   ├── src/
│   └── package.json
└── README.md
```

## Setup

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your Discogs API credentials

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Technologies Used

- Backend:
  - Python
  - Flask
  - Discogs-Client

- Frontend:
  - React
  - Bootstrap
  - Axios
