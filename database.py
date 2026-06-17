import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "school_db")

db = SQLAlchemy()
migrate = Migrate()


def init_app(app: Flask):
    """Initialize database with Flask app"""
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{int(os.getenv('DB_PORT', 3306))}/"
        f"{DB_NAME}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

def init_db(app):
    """Create tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database and tables ready")