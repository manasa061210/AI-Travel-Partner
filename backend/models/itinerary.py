from database import db
from datetime import datetime
import json

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    destination = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, default=3)
    budget = db.Column(db.Float)
    travelers = db.Column(db.Integer, default=1)
    start_date = db.Column(db.String(20))
    interests = db.Column(db.Text, default='[]')
    plan = db.Column(db.Text, default='{}')   # JSON day-by-day plan
    total_cost = db.Column(db.Float, default=0)
    hotel_category = db.Column(db.String(30), default='standard')
    transport_type = db.Column(db.String(30), default='flight')
    status = db.Column(db.String(20), default='planned')  # planned, ongoing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        plan = {}
        interests = []
        try:
            plan = json.loads(self.plan) if self.plan else {}
            interests = json.loads(self.interests) if self.interests else []
        except Exception:
            pass
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'destination': self.destination,
            'days': self.days,
            'budget': self.budget,
            'travelers': self.travelers,
            'start_date': self.start_date,
            'interests': interests,
            'plan': plan,
            'total_cost': self.total_cost,
            'hotel_category': self.hotel_category,
            'transport_type': self.transport_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
