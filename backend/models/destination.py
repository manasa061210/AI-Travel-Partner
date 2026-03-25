from database import db
import json

class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), default='India')
    city = db.Column(db.String(100))
    category = db.Column(db.String(50))  # beach, mountain, cultural, relaxation, adventure, city
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300), default='')
    base_cost_per_day = db.Column(db.Float, default=2000)
    rating = db.Column(db.Float, default=4.0)
    popular_attractions = db.Column(db.Text, default='[]')
    best_season = db.Column(db.String(100))
    weather_info = db.Column(db.Text)

    reviews = db.relationship('Review', backref='destination', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        attractions = []
        try:
            attractions = json.loads(self.popular_attractions) if self.popular_attractions else []
        except Exception:
            pass
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'base_cost_per_day': self.base_cost_per_day,
            'rating': self.rating,
            'popular_attractions': attractions,
            'best_season': self.best_season,
            'weather_info': self.weather_info,
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def to_dict(self):
        from models.user import User
        user = User.query.get(self.user_id)
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'user_name': user.name if user else 'Anonymous',
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
