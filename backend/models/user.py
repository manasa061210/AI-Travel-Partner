from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    preferences = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trips = db.relationship('Itinerary', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        prefs = {}
        try:
            prefs = json.loads(self.preferences) if self.preferences else {}
        except Exception:
            pass
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'preferences': prefs,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
