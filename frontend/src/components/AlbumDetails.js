import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, ListGroup, Badge } from 'react-bootstrap';
import axios from 'axios';

function AlbumDetails() {
  const { id } = useParams();
  const [album, setAlbum] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlbumDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/album/${id}`);
        setAlbum(response.data);
      } catch (error) {
        console.error('Error fetching album details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlbumDetails();
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!album) {
    return <div>Album not found</div>;
  }

  return (
    <div>
      <Card>
        <Card.Header>
          <h2>{album.title}</h2>
          <h4>{album.artist} - {album.year}</h4>
        </Card.Header>
        <Card.Body>
          <div className="mb-4">
            <img
              src={album.thumb || 'placeholder.jpg'}
              alt={album.title}
              style={{ maxWidth: '300px' }}
            />
          </div>

          <div className="mb-3">
            <h5>Genres:</h5>
            {album.genres.map((genre, index) => (
              <Badge key={index} bg="primary" className="me-2">
                {genre}
              </Badge>
            ))}
          </div>

          <div className="mb-3">
            <h5>Styles:</h5>
            {album.styles.map((style, index) => (
              <Badge key={index} bg="secondary" className="me-2">
                {style}
              </Badge>
            ))}
          </div>

          <h5>Tracklist:</h5>
          <ListGroup>
            {album.tracklist.map((track, index) => (
              <ListGroup.Item key={index}>
                {track.position}. {track.title} {track.duration && `(${track.duration})`}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Card.Body>
      </Card>
    </div>
  );
}

export default AlbumDetails;
