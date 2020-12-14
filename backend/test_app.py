import os
import unittest
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Artist, Client, Appointment


class TattooShopTestCase(unittest.TestCase):
    # This class represents the tattoo test case

    def setUp(self):
        # define test variables and initiate app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_tattoo_shop"
        self.database_path = "postgresql://postgres@localhost:5432/{}".format(
                                self.database_name
                                )
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    '''
    Test Get endpoints for Artists, Client, and Appointments
    '''

    def test_get_all_artists(self):
        # Test GET artists endpoint returns:
        # artits and 200 OK status
        res = self.client().get('/api/artists')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artists'])
        self.assertTrue(data['total_artists'])

    def test_get_artist_by_id(self):
        # Test GET artist according to artist_id returns:
        # artist and 200 OK status
        res = self.client().get('/api/artists/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['artist']['id'], 2)

    def test_get_all_clients(self):
        # Test GET all clients endpoint returns:
        # all clients and 200 OK status
        res = self.client().get('/api/clients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['clients'])
        self.assertTrue(data['total_clients'])

    def test_get_client_by_id(self):
        # Test GET client according to artist_id returns
        # client id and 200 OK status
        res = self.client().get('/api/clients/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['client']['id'], 2)

    def test_get_appointment_by_id(self):
        # Test GET appointment according to appt id returns:
        # appt id and 200 OK

        res = self.client().get('/api/appointments/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['appointment']['id'], 2)

    '''
    Test POST Endpoints for Artist, Client, Appointment
    '''

    def test_create_artist(self):
        # Test post request for artist endpoint returns:
        # new artist attributes and 200 OK status
        payload = {
                   'name': 'Tony Montana',
                   'phone': '123-456-7891',
                   'styles': 'Neo-Traditional',
                   'image_link': '',
                   'instagram_link': '',
                   'email': '',
                   }
        res = self.client().post('/api/artists', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artist']['id'])
        self.assertEqual(data['artist']['name'], payload['name'])
        self.assertTrue(data['total_artists'])

    def test_create_client(self):
        # Test post request for client endpoint returns:
        # new client attributes and 200 OK status
        payload = {
                   'name': '',
                   'phone': '',
                   'email': '',
                   'address': '',
                   }
        res = self.client().post('/api/clients', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['client']['id'])
        self.assertEqual(data['client']['name'], payload['name'])
        self.assertTrue(data['total_clients'])

    def test_create_appointment(self):
        # Test post request for appointment endpoint returns:
        # New appointment attributes and 200 OK status
        payload = {
                   'client': 1,
                   'artist': 1,
                   'appointment_date': datetime(2021, 3, 6, 12, 30)
                   }
        res = self.client().post('/api/appointments', json=payload)
        data = json.loads(res.data)

        last_appt = Appointment.query.all()[-1].id

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['appointment']['id'], last_appt)
        self.assertEqual(data['appointment']['artist'], payload['artist'])
        self.assertEqual(data['appointment']['client'], payload['client'])

    '''
    Test PATCH Endpoints for Artist, Client, Appointment
    '''

    def test_update_artist(self):
        # Test updating an existing artist returns: 
        # new artist and 200 OK
        payload = {
                    'phone': '901-212-4321',
                    'email': 'creative_genius@aol.com'
                   }

        res = self.client().patch('/api/artists/2', json=payload)
        data = json.loads(res.data)

        artist = Artist.query.get(2)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['artist']['id'], 2)
        self.assertEqual(data['artist']['name'], artist.name)
        self.assertEqual(data['artist']['phone'], payload['phone'])
        self.assertEqual(data['artist']['email'], payload['email'])

    def test_update_client(self):
        # Test updating an existing client returns:
        # new client and 200 OK
        payload = {
                    'phone': '770-231-4234',
                    'email': 'simplord12@gmail.com'
                    }
        res = self.client().patch('/api/clients/2', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['client']['id'], 2)
        self.assertEqual(data['client']['phone'], payload['phone'])
        self.assertEqual(data['client']['email'], payload['email'])

    def test_update_appointment(self):
        # Test updating an exisiting appointment returns:
        # new appointment and 200 OK
        payload = {
                    "appointment_date": datetime(2021, 8, 24, 2, 30)
                    }
        res = self.client().patch('/api/appointments/1', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['appointment']['id'], 1)
        self.assertEqual(datetime.strptime(data['appointment']['appointment_date'], "%a, %d %b %Y %I:%M:%S %Z"),
                         payload['appointment_date']
                         )
        
    '''
    Test Errors for GET Endpoints for Artist, Client, Appointment
    
    def test_get_all_artists_error(self):
        pass

    def test_get_artist_by_id_error(self):
        pass

    def test_get_all_clients_error(self):
        pass

    def test_get_client_by_id_error(self):
        pass
    '''

    '''
    Test Errors for POST Endpoints for Artist, Client, Appointment

    def test_create_artist_error(self):
        pass

    def test_create_client_error(self):
        pass

    def test_create_appointment_error(self):
        pass
    '''

if __name__ == '__main__':
    unittest.main()