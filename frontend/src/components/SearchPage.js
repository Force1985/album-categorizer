import React, { useState } from 'react';
import { Form, Button, Card, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import axios from 'axios';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [albums, setAlbums] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/api/search?q=${encodeURIComponent(query)}`);
      setAlbums(response.data);
    } catch (error) {
      console.error('Error searching albums:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="mb-4">Search Albums</h1>
      <Form onSubmit={handleSearch} className="mb-4">
        <Row>
          <Col md={8}>
            <Form.Control
              type="text"
              placeholder="Search for albums..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </Col>
          <Col md={4}>
            <Button variant="primary" type="submit" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </Col>
        </Row>
      </Form>

      <Row xs={1} md={2} lg={3} className="g-4">
        {albums.map((album) => (
          <Col key={album.id}>
            <Card>
              <Card.Img
                variant="top"
                src={album.thumb || 'placeholder.jpg'}
                alt={album.title}
                style={{ height: '200px', objectFit: 'cover' }}
              />
              <Card.Body>
                <Card.Title>{album.title}</Card.Title>
                <Card.Text>
                  {album.artist} - {album.year}
                </Card.Text>
                <Link to={`/album/${album.id}`} className="btn btn-primary">
                  View Details
                </Link>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default SearchPage;
