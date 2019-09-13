from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Location(db.Model):
    __tablename__ = 'location'
    name = db.Column(db.String(500), primary_key=True)
    rental_data_rel = db.relationship('RentalData',
                                      back_populates='location_rel',
                                      lazy='joined',
                                      cascade='all, delete-orphan')
    distance_matrix_data_rel = db.relationship('DistanceMatrixData',
                                               back_populates='location_rel',
                                               lazy='joined',
                                               cascade='all, delete-orphan')
    scores_rel = db.relationship('Scores',
                                 back_populates='location_rel',
                                 lazy='joined',
                                 cascade='all, delete-orphan')


class RentalData(db.Model):
    __tablename__ = 'rental_data'
    total_properties = db.Column(db.Integer, nullable=False, default=0)
    average_rent = db.Column(db.Float, nullable=True)
    rent_under_250 = db.Column(db.Integer, nullable=False, default=0)
    rent_250_to_500 = db.Column(db.Integer, nullable=False, default=0)
    datetime = db.Column(db.DateTime, default=datetime.utcnow(), primary_key=True)
    location_name = db.Column(db.String(500), db.ForeignKey('location.name'),
                              nullable=False, primary_key=True)
    location_rel = db.relationship('Location', single_parent=True,
                                   back_populates='rental_data_rel')


class DistanceMatrixData(db.Model):
    __tablename__ = 'distance_matrix_data'
    distance_to_london = db.Column(db.Integer, nullable=True, default=None)
    duration_to_london = db.Column(db.Integer, nullable=True, default=None)
    distance_to_london_text = db.Column(db.String(100), nullable=True,
                                        default=None)
    duration_to_london_text = db.Column(db.String(100), nullable=True,
                                        default=None)
    datetime = db.Column(db.DateTime, default=datetime.utcnow(),
                         primary_key=True)
    location_name = db.Column(db.String(500), db.ForeignKey('location.name'),
                              nullable=False, primary_key=True)
    location_rel = db.relationship('Location', single_parent=True,
                                   back_populates='distance_matrix_data_rel')


class Scores(db.Model):
    __tablename__ = 'scores'
    score = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow(),
                         primary_key=True)
    location_name = db.Column(db.String(500), db.ForeignKey('location.name'),
                              nullable=False, primary_key=True)
    location_rel = db.relationship('Location', single_parent=True,
                                   back_populates='scores_rel')
