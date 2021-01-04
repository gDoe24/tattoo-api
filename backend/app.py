import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
from models import setup_db, Artist, Client, Appointment
from auth.auth import requires_auth, AuthError


'''
Common functions used in the app
'''
CLIENTS_PER_PAGE = 10
# Paginate Clients


def paginate_clients(request, clients):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*CLIENTS_PER_PAGE
    end = start + CLIENTS_PER_PAGE

    format_clients = [client.format() for client in clients]
    current_clients = format_clients[start:end]

    return current_clients


# Format date string and check if correct datetime format
def format_datetime(date_time):
    if date_time is None:
        return
    try:
        return datetime.strptime(date_time, "%a, %d %b %Y %H:%M:%S %Z")
    except:
        abort(422)


# Check database for artist
def check_for_artist(artist):
    if artist is None:
        return

    check_artist = Artist.query.get(artist)
    if check_artist is None:
        abort(404)


# Check database for client
def check_for_client(client):
    if client is None:
        return

    check_client = Client.query.get(client)

    if check_client is None:
        abort(404)


# Check database for appointment
def check_for_appointment(appt):
    if appt is None:
        return

    check_appt = Appointment.query.get(appt)
    if check_appt is None:
        abort(404)


# Format an artist
def format_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return artist.format()


# Format a client
def format_client(client_id):
    client = Client.query.get(client_id)
    return client.format()


# Format an appointment
def format_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    return appt.format()


'''
# Primary handler of the application
# Contains Endpoints, CORS, Errors
'''


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
                             'POST,GET,PATCH,DELETE')
        return response

    @app.route('/')
    def index():
        return "Healthy"

    '''
    GET Endpoints for Artist, Client, Appointment
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

        # Check for artist in database
        check_for_artist(artist_id)
        # Get the artist and return formatted artist
        formatted_artist = format_artist(artist_id)

        return jsonify({
                        'success': True,
                        'artist': formatted_artist,
                        })

    # return all clients formatted
    @app.route('/api/clients')
    @requires_auth('get:all')
    def all_clients(payload):

        clients = Client.query.all()
        size = len(clients)
        if size == 0:
            abort(404)

        formatted_clients = paginate_clients(request, clients)
        if len(formatted_clients) == 0:
            abort(404)

        return jsonify({
                        'success': True,
                        'clients': formatted_clients,
                        'total_clients': size
                        })

    # Return a single client according to client id
    @app.route('/api/clients/<client_id>')
    @requires_auth('get:all')
    def single_client(payload, client_id):

        # Check for artist in database
        check_for_client(client_id)
        # Get the artist and return formatted artist
        formatted_client = format_client(client_id)

        return jsonify({
                        'success': True,
                        'client': formatted_client
                        })

    # Return a single appointment according to id
    @app.route('/api/appointments/<appt_id>')
    @requires_auth('get:appointment')
    def single_appointment(payload, appt_id):

        # Check for appointment in datbase
        check_for_appointment(appt_id)
        # Get appointment and return formatted appointment
        formatted_appt = format_appointment(appt_id)

        return jsonify({
                        'success': True,
                        'appointment': formatted_appt
                        })

    '''
    POST Endpoints for Artist, Client, Appointment
    '''
    # Post endpoint for creating artists
    @app.route('/api/artists', methods=['POST'])
    @requires_auth('create:artist')
    def create_artist(payload):
        # Get values from request
        body = request.get_json()
        name = body.get('name', None)
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

        # Update database with new artist object
        try:
            new_artist.insert()
        except:
            abort(422)

        # Find the new artist by getting the last instance of an artist
        # matching the new_artist object name
        posted_artist = Artist.query.filter(
                                            Artist.name == new_artist.name
                                            ).order_by(Artist.id).all()[-1]

        formatted_artist = posted_artist.format()
        total_artists = len(Artist.query.all())
        return jsonify({
                        'success': True,
                        'artist': formatted_artist,
                        'total_artists': total_artists
                        })

    # Post endoint for creating clients
    @app.route('/api/clients', methods=['POST'])
    @requires_auth('create:client')
    def create_client(payload):
        # Get values from request and create a new client object
        body = request.get_json()
        name = body.get('name', None)
        phone = body.get('phone', '')
        email = body.get('email', '')
        address = body.get('address', '')

        new_client = Client(
                            name=name,
                            phone=phone,
                            email=email,
                            address=address
                            )

        # Insert new client into database or return 422
        try:
            new_client.insert()
        except:
            abort(422)

        # Find the new client by getting the last instance of a client
        # matching the new_client object name
        posted_client = Client.query.filter(
                                            Client.name == new_client.name
                                            ).order_by(Client.id).all()[-1]

        formatted_client = posted_client.format()

        total_clients = len(Client.query.all())
        return jsonify({
                        'success': True,
                        'client': formatted_client,
                        'total_clients': total_clients
                        })

    # Post endoint for creating appointments
    @app.route('/api/appointments', methods=['POST'])
    @requires_auth('create:appointment')
    def create_appointment(payload):
        # Get values from the request
        body = request.get_json()
        artist_id = body.get('artist', None)
        client_id = body.get('client', None)
        appt_date = body.get('appointment_date', None)

        # Appointment will not be created if it does not
        # include an appointment date
        if appt_date is None:
            abort(422)

        appointment_date = format_datetime(appt_date)

        new_appt = Appointment(client=client_id,
                               artist=artist_id,
                               appointment_date=appointment_date
                               )
        # Insert the new appointment into the database
        try:
            new_appt.insert()
        except:
            return abort(422)

        # Get the appointment in the database by matching the artist
        # and appointment time
        posted_appt = Appointment.query.filter(
                                                Appointment.artist == new_appt.artist
                                                ).filter(
                                                        Appointment.appointment_date == new_appt.appointment_date
                                                        ).order_by(Appointment.id).all()[-1]

        formatted_appt = posted_appt.format()

        # Return an array containing all upcoming appointments
        now = datetime.now()
        upcoming_appointments = Appointment.query.filter(
                                                         Appointment.appointment_date > now
                                                         ).all()
        return jsonify({
                        'success': True,
                        'appointment': formatted_appt,
                        'total_upcoming_appointments': len(upcoming_appointments)
                        })

    '''
    PATCH Endpoints for Artist, Client, Appointment
    '''

    # Patch endpoint for updating an artist
    @app.route('/api/artists/<artist_id>', methods=['PATCH'])
    @requires_auth('update:artist')
    def update_artist(payload, artist_id):
        body = request.get_json()

        # Check database for client
        check_for_artist(artist_id)
        artist = Artist.query.get(artist_id)

        # Update artist values with new values if new values exist
        # Else keep old values
        artist.name = body.get('name', artist.name)
        artist.phone = body.get('phone', artist.phone)
        artist.styles = body.get('styles', artist.styles)
        artist.image_link = body.get('image_link', artist.image_link)
        artist.instagram_link = body.get('instagram_link', artist.instagram_link)
        artist.email = body.get('email', artist.email)

        # Update artist in database
        try:
            artist.update()
        except:
            abort(422)

        formatted_artist = format_artist(artist_id)

        return jsonify({
                        'success': True,
                        'artist': formatted_artist
                        })

    # Patch endpoint for updating a client
    @app.route('/api/clients/<client_id>', methods=['PATCH'])
    @requires_auth('update:client')
    def update_client(payload, client_id):

        body = request.get_json()
        # Check database for client
        check_for_client(client_id)
        client = Client.query.get(client_id)

        # Update client with new values if value exists
        # Else keep old values
        client.name = body.get('name', client.name)
        client.phone = body.get('phone', client.phone)
        client.email = body.get('email', client.email)
        client.address = body.get('address', client.address)

        # Update client in databse
        try:
            client.update()
        except:
            abort(422)

        formatted_client = format_client(client_id)

        return jsonify({
                        'success': True,
                        'client': formatted_client
                        })

    # Patch endpoint for updating an appointment
    @app.route('/api/appointments/<appt_id>', methods=['PATCH'])
    @requires_auth('update:appointment')
    def update_appointment(payload, appt_id):

        body = request.get_json()

        # Check database for appointment
        check_for_appointment(appt_id)
        appt = Appointment.query.get(appt_id)

        # Get artist from request and check database
        artist = body.get('artist', None)
        check_for_artist(artist)

        # Get client from request and check database
        client = body.get('client', None)
        check_for_client(client)

        # If body does not include artist/client, keep current artist/client
        appt.artist = artist if artist is not None else appt.artist
        appt.client = client if client is not None else appt.client

        # Get appointment date from request and format to datetime
        appointment_date = body.get('appointment_date', None)
        date = format_datetime(appointment_date)

        # If body does not include a new appt date, keep the current appt date
        appt.appointment_date = date if date is not None else appt.appointment_date

        # Update appointment in database
        try:
            appt.update()
        except:
            abort(422)

        formatted_appt = format_appointment(appt_id)

        return jsonify({
                        'success': True,
                        'appointment': formatted_appt
                        })

    '''
    DELETE Endpoints for Artist, Client, Appointment
    '''

    # DELETE endpoint for a single artist
    @app.route('/api/artists/<artist_id>', methods=['DELETE'])
    @requires_auth('delete:artist')
    def delete_artist(payload, artist_id):

        # Check database for artist
        check_for_artist(artist_id)
        # Get artist and delete from database
        artist = Artist.query.get(artist_id)

        try:
            artist.delete()
        except:
            abort(422)

        total_artists = Artist.query.count()

        return jsonify({
                        'success': True,
                        'deleted_artist_id': artist.id,
                        'total_artists': total_artists
                        })

    # DELETE endpoint for a single client
    @app.route('/api/clients/<client_id>', methods=['DELETE'])
    @requires_auth('delete:client')
    def delete_client(payload, client_id):

        # Check database for client
        check_for_client(client_id)
        # Get client and delete from database
        client = Client.query.get(client_id)

        try:
            client.delete()
        except:
            abort(422)

        total_clients = Client.query.count()

        return jsonify({
                        'success': True,
                        'deleted_client_id': client.id,
                        'total_clients': total_clients
                        })

    # DELETE endpoint for a single appointment
    @app.route('/api/appointments/<appt_id>', methods=['DELETE'])
    @requires_auth('delete:appointment')
    def delete_appointment(payload, appt_id):

        # Check database for appointment
        check_for_appointment(appt_id)
        # Get appointment and delete from database
        appt = Appointment.query.get(appt_id)

        try:
            appt.delete()
        except:
            abort(422)
        now = datetime.now()
        upcoming_appointments = Appointment.query.filter(
                                                         Appointment.appointment_date > now
                                                        ).all()

        return jsonify({
                        'success': True,
                        'deleted_appointment_id': appt.id,
                        'total_upcoming_appointments': len(upcoming_appointments)
                        })

    '''
    Error Handlers
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
                        'success': False,
                        'error': 401,
                        'message': 'Unauthorized request'
                        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
                        'success': False,
                        'error': 403,
                        'message': "Forbidden request"
                        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found',
        }), 404

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Request'
        }), 422

    @app.errorhandler(500)
    def unprocessable_request(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run()
