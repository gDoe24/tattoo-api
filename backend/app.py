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
                             'POST,GET,PATCH,DELETE')
        return response

    @app.route('/')
    def index():
        return jsonify({
            'date': datetime(2021, 3, 6, 12, 30)
        })

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
        
        artist = Artist.query.get(artist_id)
        if artist is None:
            abort(404)

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
        if len(formatted_clients) == 0:
            abort(404)

        return jsonify({
                        'success': True,
                        'clients': formatted_clients,
                        'total_clients': size
                        })

    # Return a single client according to client id
    @app.route('/api/clients/<client_id>')
    def single_client(client_id):
        
        client = Client.query.get(client_id)
        if client is None:
            abort(404)

        formatted_client = client.format()

        return jsonify({
                        'success': True,
                        'client': formatted_client
                        })

    # Return a single appointment according to id
    @app.route('/api/appointments/<appt_id>')
    def single_appointment(appt_id):

        
        appt = Appointment.query.get(appt_id)
        if appt is None:
            abort(404)

        formatted_appt = appt.format()

        return jsonify({
                        'success': True,
                        'appointment': formatted_appt
                        })

    '''
    POST Endpoints for Artist, Client, Appointment
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
        appointment_date = datetime.strptime(body['appointment_date'], "%a, %d %b %Y %I:%M:%S %Z")

        new_appt = Appointment(client=client_id, artist=artist_id, appointment_date=appointment_date)

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
                                                        Appointment.appointment_date == new_appt.appointment_date
                                                        ).order_by(Appointment.id).all()[-1]
        if posted_appt is None:
            abort(404)
        formatted_appt = posted_appt.format()
        return jsonify({
                        'success': True,
                        'appointment': formatted_appt
                        })

    '''
    PATCH Endpoints for Artist, Client, Appointment
    '''

    # Patch endpoint for updating an artist
    @app.route('/api/artists/<artist_id>', methods=['PATCH'])
    def update_artist(artist_id):
        body = request.get_json()
        artist = Artist.query.get(artist_id)
        artist.name = body.get('name', artist.name)
        artist.phone = body.get('phone', artist.phone)
        artist.styles = body.get('styles', artist.styles)
        artist.image_link = body.get('image_link', artist.image_link)
        artist.instagram_link = body.get('instagram_link', artist.instagram_link)
        artist.email = body.get('email', artist.email)

        try:
            artist.update()
        except:
            abort(422)

        updated_artist = Artist.query.get(artist_id)
        formatted_artist = updated_artist.format()

        return jsonify({
                        'success': True,
                        'artist': formatted_artist
                        })

    # Patch endpoint for updating a client
    @app.route('/api/clients/<client_id>', methods=['PATCH'])
    def update_client(client_id):

        body = request.get_json()
        client = Client.query.get(client_id)

        client.name = body.get('name', client.name)
        client.phone = body.get('phone', client.phone)
        client.email = body.get('email', client.email)
        client.address = body.get('address', client.address)

        try:
            client.update()
        except:
            abort(422)

        updated_client = Client.query.get(client_id)
        formatted_client = updated_client.format()

        return jsonify({
                        'success': True,
                        'client': formatted_client
                        })

    # Patch endpoint for updating an appointment
    @app.route('/api/appointments/<appt_id>', methods=['PATCH'])
    def update_appointment(appt_id):
        
        body = request.get_json()
        appt = Appointment.query.get(appt_id)

        appt.artist = body.get('name', appt.artist)
        appt.client = body.get('phone', appt.client)

        if body['appointment_date'] is not None:
            date = datetime.strptime(body['appointment_date'], "%a, %d %b %Y %I:%M:%S %Z")
        else:
            date = appt.appointment_date
        appt.appointment_date = date

        try:
            appt.update()
        except:
            abort(422)
        
        updated_appt = Appointment.query.get(appt_id)
        formatted_appt = updated_appt.format()

        return jsonify({
                        'success': True,
                        'appointment': formatted_appt
                        })

    '''
    DELETE Endpoints for Artist, Client, Appointment
    '''

    # DELETE endpoint for a single artist
    @app.route('/api/artists/<artist_id>', methods=['DELETE'])
    def delete_artist(artist_id):

        artist = Artist.query.get(artist_id)
        if artist is None:
            abort(404)
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
    def delete_client(client_id):
        client = Client.query.get(client_id)
        if client is None:
            abort(404)
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
    def delete_appointment(appt_id):

        appt = Appointment.query.get(appt_id)
        if appt is None:
            abort(404)
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
    APP.run(host='0.0.0.0', port=8080, debug=True)
