from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import db, init_db
from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)
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

    init_db(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=5000)
