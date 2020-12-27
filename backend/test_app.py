import os
import unittest
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Artist, Client, Appointment
from config import MANAGER_JWT, CLIENT_JWT, ARTIST_JWT


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
        self.manager_jwt = MANAGER_JWT
        self.client_jwt = CLIENT_JWT
        self.artist_jwt = ARTIST_JWT
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
        res = self.client().get('/api/clients',
                                headers={
                                        "Authorization": self.manager_jwt
                                        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['clients'])
        self.assertTrue(data['total_clients'])

    def test_get_client_by_id(self):
        # Test GET client according to artist_id returns
        # client id and 200 OK status
        res = self.client().get('/api/clients/2',
                                headers={
                                         "Authorization": self.manager_jwt
                                         })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['client']['id'], 2)

    def test_get_appointment_by_id(self):
        # Test GET appointment according to appt id returns:
        # appt id and 200 OK

        res = self.client().get('/api/appointments/2',
                                headers={
                                        "Authorization": self.manager_jwt
                                        })
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

        res = self.client().post('/api/artists',
                                 headers={"Authorization": self.manager_jwt},
                                 json=payload
                                 )
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
                   'name': 'Joe Schmo',
                   'phone': '',
                   'email': '',
                   'address': '',
                   }
        res = self.client().post('/api/clients',
                                 json=payload,
                                 headers={"Authorization": self.manager_jwt}
                                 )
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
        res = self.client().post('/api/appointments',
                                 json=payload,
                                 headers={"Authorization": self.manager_jwt}
                                 )
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

        res = self.client().patch('/api/artists/2',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
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
        res = self.client().patch('/api/clients/2',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
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
        res = self.client().patch('/api/appointments/1',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['appointment']['id'], 1)
        self.assertEqual(datetime.strptime(
                                           data['appointment']['appointment_date'],
                                           "%a, %d %b %Y %I:%M:%S %Z"
                                           ),
                         payload['appointment_date']
                         )

    '''
    Test DELETE Endpoints for artists, clients, appointments
    '''

    def test_delete_artist(self):
        # Test sending a delete method for an existing artist returns:
        # id of the deleted artist and 200 OK
        artist_id = Artist.query.order_by(Artist.id).all()[-1].id
        res = self.client().delete(f"/api/artists/{artist_id}",
                                   headers={"Authorization": self.manager_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_artist_id'], artist_id)
        self.assertTrue(data['total_artists'])

    def test_delete_client(self):
        # Test sending a delete method for an existing client returns:
        # id of the deleted client and 200 OK
        client_id = Client.query.order_by(Client.id).all()[-1].id
        res = self.client().delete(f"/api/clients/{client_id}",
                                   headers={"Authorization": self.manager_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_client_id'], client_id)
        self.assertTrue(data['total_clients'])

    def test_delete_appointment(self):
        # Test sending a delete method for an existing appointment returns:
        # id of the deleted appointment and 200 OK
        appt_id = Appointment.query.order_by(Appointment.id).all()[-1].id
        res = self.client().delete(f"/api/appointments/{appt_id}",
                                   headers={"Authorization": self.manager_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_appointment_id'], appt_id)
        self.assertTrue(data['total_upcoming_appointments'])

    '''
    Test Errors for GET Endpoints for Artist, Client, Appointment
    '''
    # Test a request for bad url returns 404 message
    def test_get_all_artists_error(self):

        res = self.client().get('/artists')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test a request for artist that does not exist returns 404
    def test_get_artist_by_id_error(self):

        res = self.client().get('/api/artists/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test request for clients page that does not exist returns 404
    def test_get_all_clients_error(self):

        res = self.client().get('/api/clients?page=1000',
                                headers={"Authorization": self.manager_jwt}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test request for client that does not exist returns 404
    def test_get_client_by_id_error(self):

        res = self.client().get('/api/clients/10000',
                                headers={"Authorization": self.manager_jwt}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test request for appointment that does not exist returns 404
    def test_get_appointment_by_id_error(self):

        res = self.client().get('/api/appointments/10000',
                                headers={"Authorization": self.manager_jwt}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    '''
    Test Errors for POST Endpoints for Artist, Client, Appointment
    '''
    # Test creating an artist without a name returns a 422 error
    def test_create_artist_error(self):

        payload = {
                   'phone': '123-456-7891',
                   'styles': 'Neo-Traditional',
                   'image_link': '',
                   'instagram_link': '',
                   'email': '',
                   }
        res = self.client().post('/api/artists',
                                 json=payload,
                                 headers={"Authorization": self.manager_jwt}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test creating an client without a name returns a 422 error
    def test_create_client_error(self):
        payload = {
                   'phone': '',
                   'email': '',
                   'address': '',
                   }
        res = self.client().post('/api/clients',
                                 json=payload,
                                 headers={"Authorization": self.manager_jwt}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test creating appointment without date returns 422 error
    def test_create_appointment_error(self):
        payload = {
                   'client': 1,
                   'artist': 1,
                   }
        res = self.client().post('/api/appointments',
                                 json=payload,
                                 headers={"Authorization": self.manager_jwt}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    '''
    Test Errors for PATCH Endpoints for Artist, Client, Appointment
    '''

    # Test updating an arist which does not exist returns a 404 error
    def test_update_artist_error(self):

        payload = {
                   'name': 'John Deer',
                   'phone': '123-456-7891',
                   'styles': 'Neo-Traditional',
                   'image_link': '',
                   'instagram_link': '',
                    }
        res = self.client().patch('/api/artists/1000',
                                  headers={"Authorization": self.manager_jwt}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test updating a client which does not exist returns a 404 error
    def test_update_client_error(self):
        payload = {
                   'name': 'John',
                   'phone': '',
                   'email': '',
                   'address': '',
                   }
        res = self.client().patch('/api/clients/1000',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test using the wrong appointment format returns a 422 error
    def test_update_appointment_error(self):
        payload = {
                    'appointment_date': "2020, 12 31, 12:30:54"
                    }

        res = self.client().patch('/api/appointments/2',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test updating the appointment with non existent artist returns
    # 404 error
    def test_update_appointment_artist_error(self):
        payload = {
                    'artist': 1000
                    }

        res = self.client().patch('/api/appointments/2',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test updating the appointment with non existent client returns
    # 404 error
    def test_update_appointment_client_error(self):
        payload = {
                    'client': 1000
                    }

        res = self.client().patch('/api/appointments/2',
                                  json=payload,
                                  headers={"Authorization": self.manager_jwt}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    '''
    Test Errors for DELETE Endpoints for Artist, Client, Appointment
    '''
    # Test deleting artist that does not exist return 404
    def test_delete_artist_error(self):

        res = self.client().delete('/api/artists/1000',
                                   headers={"Authorization": self.manager_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test deleting client that does not exist return 404
    def test_delete_client_error(self):
        res = self.client().delete('/api/clients/1000',
                                   headers={"Authorization": self.manager_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test deleting appointment that does not exist return 404
    def test_delete_appointment_error(self):
        res = self.client().delete('/api/appointments/1000',
                                   headers={"Authorization": self.manager_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    '''
    Test Role Based Authentication
    '''

    # Test Client can view a single appointment
    def test_client_view_appointment(self):

        res = self.client().get('/api/appointments/2',
                                headers={"Authorization": self.client_jwt}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['appointment']['id'], 2)

    # Test Client forbidden to update an appointment
    def test_client_update_appointment_unauthorized(self):

        payload = {
                    "artist": 2
                   }
        res = self.client().patch('/api/appointments/2',
                                  json=payload,
                                  headers={
                                           "Authorization": self.client_jwt
                                           }
                                  )
        data = json.loads(res.data)

        self.assertTrue(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Test artist can update an appointment
    def test_artist_update_appointment(self):

        payload = {
                    'appointment_date': datetime(2021, 4, 6, 3, 30)
                    }
        res = self.client().patch('/api/appointments/2',
                                  json=payload,
                                  headers={
                                           "Authorization": self.artist_jwt
                                           }
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(datetime.strptime(
                                           data['appointment']['appointment_date'],
                                           "%a, %d %b %Y %I:%M:%S %Z"
                                           ),
                         payload['appointment_date']
                         )

    # Test artist unable to delete a client
    def test_artist_delete_client_unauthorized(self):

        res = self.client().delete('/api/clients/2',
                                   headers={"Authorization": self.artist_jwt}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


if __name__ == '__main__':
    unittest.main()
