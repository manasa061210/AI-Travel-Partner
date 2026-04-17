from flask import Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS
from config import Config
from database import db, init_db
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REACT_BUILD = os.path.join(BASE_DIR, 'static_react')


def create_app():
    app = Flask(__name__, static_folder=REACT_BUILD, static_url_path='')
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.destinations import destinations_bp
    from routes.admin import admin_bp
    from routes.ai_routes import ai_bp

    app.register_blueprint(auth_bp,         url_prefix='/api/auth')
    app.register_blueprint(user_bp,         url_prefix='/api/user')
    app.register_blueprint(destinations_bp, url_prefix='/api/destinations')
    app.register_blueprint(admin_bp,        url_prefix='/api/admin')
    app.register_blueprint(ai_bp,           url_prefix='/api/ai')

    # Health check
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok', 'message': 'Travel Partner API is running'})

    # Serve React frontend for all non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path and os.path.exists(os.path.join(REACT_BUILD, path)):
            return send_from_directory(REACT_BUILD, path)
        return send_from_directory(REACT_BUILD, 'index.html')

    init_db(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=False, port=5000)
