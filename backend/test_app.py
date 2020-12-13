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

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['appointment']['id'])
        self.assertEqual(data['appointment']['artist'], payload['artist'])
        self.assertEqual(data['appointment']['client'], payload['client'])
        
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

if __name__ == '__main__':
    unittest.main()