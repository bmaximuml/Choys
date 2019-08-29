from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Location(db.Model):
    name = db.Column(db.String(500), primary_key=True)
    rental_data = db.relationship('RentalData', backref='location', lazy=True)
    distance_matrix_data = db.relationship('DistanceMatrixData', backref='location', lazy=True)
    scores = db.relationship('Scores', backref='location', lazy=True)


class RentalData(db.Model):
    total_properties = db.Column(db.Integer, nullable=False, default=0)
    average_rent = db.Column(db.Integer, nullable=True)
    rent_under_250 = db.Column(db.Integer, nullable=False, default=0)
    rent_250_to_500 = db.Column(db.Integer, nullable=False, default=0)
    datetime = db.Column(db.DateTime, default=datetime.utcnow(), primary_key=True)
    location_name = db.Column(db.String(500), db.ForeignKey('location.name'), nullable=False, primary_key=True)


class DistanceMatrixData(db.Model):
    distance_to_london = db.Column(db.Integer, nullable=True, default=None)
    duration_to_london = db.Column(db.Integer, nullable=True, default=None)
    distance_to_london_text = db.Column(db.String(100), nullable=True, default=None)
    duration_to_london_text = db.Column(db.String(100), nullable=True, default=None)
    datetime = db.Column(db.DateTime, default=datetime.utcnow(), primary_key=True)
    location_name = db.Column(db.String(500), db.ForeignKey('location.name'), nullable=False, primary_key=True)


class Scores(db.Model):
    score = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow(), primary_key=True)
    location_name = db.Column(db.String(500), db.ForeignKey('location.name'), nullable=False, primary_key=True)
