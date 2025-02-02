from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    user_psw = db.Column(db.String(255), nullable=False)  # Increased length for hashing
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        """Hash and store the user's password."""
        self.user_psw = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.user_psw, password)
