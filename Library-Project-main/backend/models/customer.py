from . import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)