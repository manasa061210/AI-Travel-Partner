import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'travel-partner-secret-key-2026')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'travel-jwt-secret-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///travel_partner.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
