import sqlite3
import json
import os

# Put the database file in the app directory
DB_PATH = os.path.join(os.path.dirname(__file__), "verification_cache.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def init_db():
    """Creates the cache table if it doesn't exist yet."""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS beneficiary_cache (
                rc_no TEXT PRIMARY KEY,
                details TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def get_cached_beneficiary(rc_no):
    """Looks up a ration card number in the local SQLite database."""
    init_db()  # Quick safety check
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT details FROM beneficiary_cache WHERE rc_no = ?", 
            (str(rc_no).strip(),)
        ).fetchone()
        
        if row:
            return json.loads(row["details"])
    return None

def save_beneficiary_to_cache(rc_no, details_dict):
    """Saves or updates a beneficiary record in the database."""
    init_db()
    with get_db_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO beneficiary_cache (rc_no, details, cached_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (str(rc_no).strip(), json.dumps(details_dict)))
        conn.commit()