from flask import Blueprint, jsonify, request
import discogs_client
import os

main = Blueprint('main', __name__)

# Initialize Discogs client
d = discogs_client.Client(
    'AlbumCategorizer/1.0',
    user_token=os.getenv('DISCOGS_TOKEN')
)

@main.route('/api/search', methods=['GET'])
def search_albums():
    query = request.args.get('q', '')
    try:
        results = d.search(query, type='release')
        albums = []
        for r in results[:10]:  # Limit to 10 results
            albums.append({
                'id': r.id,
                'title': r.title,
                'year': r.year,
                'thumb': r.thumb,
                'artist': r.artists[0].name if r.artists else 'Unknown Artist'
            })
        return jsonify(albums)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/album/<int:album_id>', methods=['GET'])
def get_album_details(album_id):
    try:
        release = d.release(album_id)
        album_data = {
            'id': release.id,
            'title': release.title,
            'artist': release.artists[0].name if release.artists else 'Unknown Artist',
            'year': release.year,
            'genres': release.genres,
            'styles': release.styles,
            'thumb': release.thumb,
            'tracklist': [{'position': t.position, 'title': t.title, 'duration': t.duration} 
                         for t in release.tracklist]
        }
        return jsonify(album_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
