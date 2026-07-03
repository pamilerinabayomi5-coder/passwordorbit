import sqlite3
from datetime import datetime
from config import DATABASE_NAME, logger

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if tables do not exist."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    join_date TEXT
                )
            """)
            
            # Preferences Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    telegram_id INTEGER PRIMARY KEY,
                    length INTEGER DEFAULT 16,
                    uppercase INTEGER DEFAULT 1,
                    lowercase INTEGER DEFAULT 1,
                    numbers INTEGER DEFAULT 1,
                    symbols INTEGER DEFAULT 1,
                    exclude_ambiguous INTEGER DEFAULT 0,
                    quantity INTEGER DEFAULT 1,
                    FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
                )
            """)
            conn.commit()
            logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}", exc_info=True)

def add_user_if_not_exists(telegram_id: int, username: str | None, first_name: str):
    """Inserts user record and default preferences if they don't exist."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (telegram_id, username, first_name, join_date) VALUES (?, ?, ?, ?)",
                (telegram_id, username, first_name, datetime.utcnow().isoformat())
            )
            cursor.execute(
                "INSERT OR IGNORE INTO preferences (telegram_id) VALUES (?)",
                (telegram_id,)
            )
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error adding user {telegram_id}: {e}", exc_info=True)

def get_user_preferences(telegram_id: int) -> dict:
    """Retrieves a user's configuration preference dictionary."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM preferences WHERE telegram_id = ?", (telegram_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            
            # Fallback dynamic insertion if missing
            add_user_if_not_exists(telegram_id, None, "User")
            cursor.execute("SELECT * FROM preferences WHERE telegram_id = ?", (telegram_id,))
            return dict(cursor.fetchone())
    except sqlite3.Error as e:
        logger.error(f"Error fetching preferences for {telegram_id}: {e}", exc_info=True)
        return {"length": 16, "uppercase": 1, "lowercase": 1, "numbers": 1, "symbols": 1, "exclude_ambiguous": 0, "quantity": 1}

def update_user_preference(telegram_id: int, column: str, value: int):
    """Updates a single key value in the user preferences row safely."""
    allowed_columns = ["length", "uppercase", "lowercase", "numbers", "symbols", "exclude_ambiguous", "quantity"]
    if column not in allowed_columns:
        raise ValueError(f"Invalid column name assignment attempted: {column}")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE preferences SET {column} = ? WHERE telegram_id = ?", (value, telegram_id))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating column {column} for user {telegram_id}: {e}", exc_info=True)
