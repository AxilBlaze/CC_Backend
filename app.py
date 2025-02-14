from flask import Flask
from flask_cors import CORS
from config.config import Config
from database import init_db
from extensions import mongo
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()  # Load environment variables
    app = Flask(__name__)
    app.config.from_object(Config)

    # Update CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })

    # Configure MongoDB with Atlas connection string from environment variable
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    mongo.init_app(app)

    # Test MongoDB connection
    try:
        # The ping command is cheap and does not require auth
        mongo.db.command('ping')
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection error: {e}")

    # Initialize database
    init_db(app)

    # Import and register blueprints
    from routes.user_routes import user_bp
    from routes.course_routes import course_bp
    from routes.recommendation_routes import recommendation_bp
    from routes.tutor_routes import tutor_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(course_bp, url_prefix='/api/courses')
    app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
    app.register_blueprint(tutor_bp, url_prefix='/api/tutor')

    return app

# Make sure Gunicorn can find 'app'
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
