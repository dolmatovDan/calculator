import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom database exceptions
class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails"""
    pass

class DatabaseQueryError(DatabaseError):
    """Raised when database query fails"""
    pass

class DatabaseInitializationError(DatabaseError):
    """Raised when database initialization fails"""
    pass

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage', 'calculations.db')

def _connect():
    """Create a database connection with error handling"""
    try:
        # ensure directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        logger.info(f"Successfully connected to database at {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError(f"Failed to connect to database: {e}")
    except OSError as e:
        logger.error(f"File system error creating database directory: {e}")
        raise DatabaseConnectionError(f"Failed to create database directory: {e}")

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = None
    try:
        conn = _connect()
        cursor = conn.cursor()

        # Create table for storing echo strings
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS echo_strings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
        raise DatabaseInitializationError(f"Failed to initialize database: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        if conn:
            conn.rollback()
        raise DatabaseInitializationError(f"Unexpected error during database initialization: {e}")
    finally:
        if conn:
            conn.close()

def save_string(text: str) -> int:
    """Save a string to the database and return the ID"""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty or None")
    
    conn = None
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO echo_strings (text) VALUES (?)', (text.strip(),))
        conn.commit()
        new_id = cursor.lastrowid
        logger.info(f"Successfully saved string with ID: {new_id}")
        return new_id if new_id is not None else -1
    except sqlite3.Error as e:
        logger.error(f"Database error saving string: {e}")
        if conn:
            conn.rollback()
        raise DatabaseQueryError(f"Failed to save string to database: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving string: {e}")
        if conn:
            conn.rollback()
        raise DatabaseQueryError(f"Unexpected error saving string: {e}")
    finally:
        if conn:
            conn.close()

def get_all_strings() -> List[Dict[str, str]]:
    """Retrieve all strings from the database"""
    conn = None
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text, created_at FROM echo_strings ORDER BY id DESC")
        rows = cursor.fetchall()
        result = [{'id': str(r[0]), 'text': r[1], 'created_at': r[2]} for r in rows]
        logger.info(f"Successfully retrieved {len(result)} strings from database")
        return result
    except sqlite3.Error as e:
        logger.error(f"Database error retrieving strings: {e}")
        raise DatabaseQueryError(f"Failed to retrieve strings from database: {e}")
    except Exception as e:
        logger.error(f"Unexpected error retrieving strings: {e}")
        raise DatabaseQueryError(f"Unexpected error retrieving strings: {e}")
    finally:
        if conn:
            conn.close()

def delete_all_strings() -> int:
    """Delete all strings from the database and return count of deleted records"""
    conn = None
    try:
        conn = _connect()
        cursor = conn.cursor()

        # Get count before deletion
        cursor.execute('SELECT COUNT(*) FROM echo_strings')
        count = cursor.fetchone()[0]

        # Delete all records
        cursor.execute('DELETE FROM echo_strings')
        conn.commit()
        
        logger.info(f"Successfully deleted {count} strings from database")
        return count
    except sqlite3.Error as e:
        logger.error(f"Database error deleting strings: {e}")
        if conn:
            conn.rollback()
        raise DatabaseQueryError(f"Failed to delete strings from database: {e}")
    except Exception as e:
        logger.error(f"Unexpected error deleting strings: {e}")
        if conn:
            conn.rollback()
        raise DatabaseQueryError(f"Unexpected error deleting strings: {e}")
    finally:
        if conn:
            conn.close()

def save_calculation(expression: str, result: str) -> int:
    if not expression or not expression.strip():
        raise ValueError("Expression cannot be empty")
    conn = None
    try:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO calculations (expression, result, created_at) VALUES (?, ?, ?)",
            (expression.strip(), str(result), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        return cur.lastrowid or -1
    except sqlite3.Error as e:
        if conn: conn.rollback()
        raise DatabaseQueryError(f"Failed to save calculation: {e}")
    finally:
        if conn: conn.close()

def get_all_calculations() -> List[Dict[str, str]]:
    conn = None
    try:
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, expression, result, created_at FROM calculations ORDER BY id DESC"
        )
        rows = cur.fetchall()
        return [
            {"id": str(r[0]), "expression": r[1], "result": r[2], "created_at": r[3]}
            for r in rows
        ]
    except sqlite3.Error as e:
        raise DatabaseQueryError(f"Failed to retrieve calculations: {e}")
    finally:
        if conn: conn.close()

def delete_all_calculations() -> int:
    conn = None
    try:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM calculations")
        count = cur.fetchone()[0]
        cur.execute("DELETE FROM calculations")
        conn.commit()
        return count
    except sqlite3.Error as e:
        if conn: conn.rollback()
        raise DatabaseQueryError(f"Failed to delete calculations: {e}")
    finally:
        if conn: conn.close()
