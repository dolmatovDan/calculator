import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage', 'calculations.db')

def _connect():
    # ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = _connect()
    cursor = conn.cursor()

    # Create table for storing echo strings
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS echo_strings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

def save_string(text: str) -> int:
    """Save a string to the database and return its new ID"""
    conn = _connect()
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    cursor.execute('INSERT INTO echo_strings (text, created_at) VALUES (?, ?)', (text, created_at))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_strings() -> List[Dict[str, str]]:
    """Return all strings from the database ordered by newest first"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, created_at FROM echo_strings ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{'id': r[0], 'text': r[1], 'created_at': r[2]} for r in rows]

def delete_all_strings() -> int:
    """Delete all strings from the database and return count of deleted records"""
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM echo_strings')
    count = cursor.fetchone()[0]

    cursor.execute('DELETE FROM echo_strings')
    conn.commit()
    conn.close()

    return count
