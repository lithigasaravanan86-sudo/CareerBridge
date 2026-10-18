import os
import sqlite3
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from database.seed_data import seed_database

def get_db_connection():
    """Returns a SQLite connection with Row factory and foreign keys enabled."""
    db_path = Config.DATABASE_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(force_reseed=False):
    """Initializes schema and seeds baseline data."""
    db_path = Config.DATABASE_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    conn = get_db_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print("Schema successfully applied.")
        seed_database(conn)
        print("CareerBridge database initialized and seeded successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error during database initialization: {e}")
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
