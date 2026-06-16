import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "school_db")
print("DB_USER:", os.getenv("DB_USER"))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def init_db():
    """Create database and tables if they don't exist."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cursor.execute(f"USE `{DB_NAME}`")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                class_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150),
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_member_class
                    FOREIGN KEY (class_id)
                    REFERENCES classes(id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()

        cursor.close()
        conn.close()

        print("✅ Database and tables ready")

    except mysql.connector.Error as err:
        print(f"❌ Database initialization error: {err}")


def get_db_connection():
    """Return a connection to the selected database."""
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_NAME
    )