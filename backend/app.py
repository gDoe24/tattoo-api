import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Artist, Client, Appointment



# Primary handler of the application
# Contains Endpoints, CORS, Errors
def create_app(test_config=None):

    # create and configure the app, database, and CORS headers
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('ACCESS-CONTROL-ALLOW-HEADERS',
                             'Content-Type,Authorization,true')
        response.headers.add('ACCESS-CONTROL-ALLOW-METHODS',
                             'POST,GET,PATCH,DELETE,PUT')
        return response

    @app.route('/')
    def index():
        return "Hello Motto"

    # Endpoint to GET all artists
    @app.route('/api/artists')
    def all_artists():
        artists = [artist.format() for artist in Artist.query.all()]

        return jsonify({
                        'success': True,
                        'artists': artists,
                        'total_artists': len(artists)
                        })
    # Return a single artist according to artist id
    @app.route('/api/artists/<artist_id>')
    def single_artist(artist_id):

        artist = Artist.query.filter(Artist.id == artist_id).one_or_none()

        if artist is None:
            return jsonify({
                            'success': False,
                            'message': 'Artist not found in database'
                            })

        formatted_artist = artist.format()
        return jsonify({
                        'success': True,
                        'artist': formatted_artist,
                        })

    # return all clients formatted
    @app.route('/api/clients')
    def all_clients():
        formatted_clients = [client.format() for client in Client.query.all()]
        return jsonify({
                        'success': True,
                        'clients': formatted_clients,
                        'total_clients': len(formatted_clients)
                        })

    # Return a single client according to client id
    @app.route('/api/clients/<client_id>')
    def single_client(client_id):

        client = Client.query.filter(Client.id == client_id).one_or_none()

        if client is None:
            return jsonify({
                            'success': False,
                            'message': "Could not locate Client in the database"
                            })

        formatted_client = client.format()

        return jsonify({
                        'success': True,
                        'client': formatted_client
                        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
