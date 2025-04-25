import sqlite3

DATABASE_NAME = "data.db"

def get_db_connection():
    """Creates and returns a new database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    return conn

def init_db():
    """Initializes the database with a metadata table to track uploads"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Table to store metadata about uploaded CSV files
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS csv_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Initialize DB on import
init_db()
