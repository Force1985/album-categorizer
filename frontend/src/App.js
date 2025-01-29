import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import SearchPage from './components/SearchPage';
import AlbumDetails from './components/AlbumDetails';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/album/:id" element={<AlbumDetails />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
