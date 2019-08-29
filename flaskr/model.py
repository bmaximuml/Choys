from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Locations(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    location_name = db.Column(db.String(500))
    total_properties = db.Column(db.Integer, nullable=False, default=0)
    average_rent = db.Column(db.Integer, nullable=True)
    rent_under_250 = db.Column(db.Integer, nullable=False, default=0)
    rent_250_to_500 = db.Column(db.Integer, nullable=False, default=0)
    newest = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, location_name, total_properties, average_rent, rent_under_250, rent_250_to_500, newest):
        self.location_name = location_name
        self.total_properties = total_properties
        self.average_rent = average_rent
        self.rent_under_250 = rent_under_250
        self.rent_250_to_500 = rent_250_to_500
        self.newest = newest


