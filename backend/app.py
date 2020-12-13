import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
from models import setup_db, Artist, Client, Appointment



CLIENTS_PER_PAGE = 10
# Paginate Clients
def paginate_clients(request, clients):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*CLIENTS_PER_PAGE
    end = start + CLIENTS_PER_PAGE

    format_clients = [client.format() for client in clients]
    current_clients = format_clients[start:end]

    return current_clients

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

    '''
    GET
    '''
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

        clients = Client.query.all()
        size = len(clients)
        if size == 0:
            abort(404)

        formatted_clients = paginate_clients(request, clients)

        return jsonify({
                        'success': True,
                        'clients': formatted_clients,
                        'total_clients': size
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

    '''
    CREATE
    '''
    # Post endpoint for creating artists
    @app.route('/api/artists', methods=['POST'])
    def create_artist():
        body = request.get_json()
        name = body.get('name')
        phone = body.get('phone', '')
        styles = body.get('styles', '')
        image_link = body.get('image_link', '')
        instagram_link = body.get('instagram_link', '')
        email = body.get('email', '')

        new_artist = Artist(
                            name=name,
                            phone=phone,
                            styles=styles,
                            image_link=image_link,
                            instagram_link=instagram_link,
                            email=email
                            )

        try:
            new_artist.insert()
        except:
            abort(422)

        posted_artist = Artist.query.filter(
                                            Artist.name == new_artist.name
                                            ).order_by(Artist.id).all()[-1]

        if posted_artist is None:
            abort(404)

        formatted_artist = posted_artist.format()
        total_artists = len(Artist.query.all())
        return jsonify({
                        'success': True,
                        'artist': formatted_artist,
                        'total_artists': total_artists
                        })

    # Post endoint for creating clients
    @app.route('/api/clients', methods=['POST'])
    def create_client():
        body = request.get_json()
        name = body['name']
        phone = body.get('phone', '')
        email = body.get('email', '')
        address = body.get('address', '')

        new_client = Client(
                            name=name,
                            phone=phone,
                            email=email,
                            address=address
                            )

        try:
            new_client.insert()
        except:
            abort(422)

        posted_client = Client.query.filter(
                                            Client.name == new_client.name
                                            ).order_by(Client.id).all()[-1]

        formatted_client = posted_client.format()
        if posted_client is None:
            abort(404)
        total_clients = len(Client.query.all())
        return jsonify({
                        'success': True,
                        'client': formatted_client,
                        'total_clients': total_clients
                        })

    # Post endoint for creating appointments
    @app.route('/api/appointments', methods=['POST'])
    def create_appointment():
        body = request.get_json()
        artist_id = body['artist']
        client_id = body['client']
        appointment_date = datetime(body['appointment_date'])

        new_appt = Appointment(
                                client=client_id,
                                artist=artist_id,
                                appointment_date=appointment_date
                              )

        try:
            new_appt.insert()
        except:
            return jsonify({
                            'success': False,
                            'message': 'Error posting new appointment'
                            })

        posted_appt = Appointment.query.filter(
                                                Appointment.artist == new_appt.artist
                                               ).filter(
                                                        Appointment.client == new_appt.client
                                                        ).filter(
                                                            Appointment.appointment_date == new_appt.appointment_date
                                                        ).query_by(Appointment.id).all()[-1]
        if posted_appt is None:
            abort(404)
        formatted_appt = posted_appt.format()
        return jsonify({
                        'success': True,
                        'appointment': formatted_appt
                        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
