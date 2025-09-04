#!/usr/bin/env python3
"""
Simple script to view the contents of the echo_strings database
"""

import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage', 'calculations.db')

def view_database():
    """View all records in the calculations database"""
    if not os.path.exists(DB_PATH):
        print("Database file does not exist yet. Run the server first to create it.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all records
    cursor.execute('SELECT id, text, created_at FROM echo_strings ORDER BY created_at DESC')
    records = cursor.fetchall()
    
    if not records:
        print("No records found in the database.")
    else:
        print(f"Found {len(records)} records in the database:")
        print("-" * 80)
        print(f"{'ID':<5} {'Text':<30} {'Created At':<20}")
        print("-" * 80)
        
        for record in records:
            id_val, text, created_at = record
            # Truncate long text for display
            display_text = text[:27] + "..." if len(text) > 30 else text
            print(f"{id_val:<5} {display_text:<30} {created_at:<20}")
    
    conn.close()

if __name__ == "__main__":
    view_database()