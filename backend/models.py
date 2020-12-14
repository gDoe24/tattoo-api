import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json


database_name = "tattoo_shop"
database_path = f"postgres://{'localhost:5432'}/{database_name}"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    phone = db.Column(db.String(120))
    styles = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    instagram_link = db.Column(db.String(500))
    email = db.Column(db.String(300))
    # One to Many relationship with appointments
    appointments = db.relationship('Appointment', backref='artist_appt_id',
                                   lazy=True
                                   )

    def __init__(self, name, phone='', styles='', image_link='', instagram_link='', email=''):
        self.name = name
        self.phone = phone
        self.styles = styles
        self.image_link = image_link
        self.instagram_link = instagram_link
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
                'id': self.id,
                'name': self.name,
                'phone': self.phone,
                'styles': self.styles,
                'email': self.email
                }


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(120))
    email = db.Column(db.String(240))
    address = db.Column(db.String(240))
    # One To Many relationship with appointments
    appointments = db.relationship('Appointment', backref='client_appt_id',
                                   lazy=True
                                   )

    def __init__(self, name, phone='', email='', address=''):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
                'id': self.id,
                'name': self.name,
                'email': self.email
                }


class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, db.ForeignKey("clients.id"))
    artist = db.Column(db.Integer, db.ForeignKey("artists.id"))
    appointment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        artist = Artist.query.filter(Artist.id == self.artist).one_or_none()
        client = Client.query.filter(Client.id == self.client).one_or_none()
        return {
                'id': self.id,
                'artist': artist.id,
                'client': client.id,
                'appointment_date': self.appointment_date
                }
