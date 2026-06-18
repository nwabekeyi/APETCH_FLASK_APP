from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app: Flask):
    """Initialize database and extensions with Flask app, then create tables"""
    # Note: app.config["SQLALCHEMY_DATABASE_URI"] is already loaded from Config in app.py
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create tables automatically within the application context
    with app.app_context():
        db.create_all()
        print("✅ Database and tables ready")