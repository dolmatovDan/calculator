import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage', 'calculations.db')

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table for storing echo strings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS echo_strings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_string(text: str) -> int:
    """Save a string to the database and return the ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO echo_strings (text) VALUES (?)
    ''', (text,))
    
    string_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return string_id

def get_string(string_id: int) -> dict:
    """Get a string by ID from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, text, created_at FROM echo_strings WHERE id = ?
    ''', (string_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "text": result[1],
            "created_at": result[2]
        }
    return None

def get_all_strings() -> list:
    """Get all strings from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, text, created_at FROM echo_strings ORDER BY created_at DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "text": row[1],
            "created_at": row[2]
        }
        for row in results
    ]

def delete_all_strings() -> int:
    """Delete all strings from the database and return count of deleted records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get count before deletion
    cursor.execute('SELECT COUNT(*) FROM echo_strings')
    count = cursor.fetchone()[0]
    
    # Delete all records
    cursor.execute('DELETE FROM echo_strings')
    
    conn.commit()
    conn.close()
    
    return count