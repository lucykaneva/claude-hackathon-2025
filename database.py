import sqlite3
import json
from datetime import datetime

DB_NAME = 'gifts_database.db'

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Gifts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donnor_name TEXT NOT NULL,
            donnor_contact TEXT NOT NULL,
            donor_address TEXT NOT NULL,
            gift_name TEXT NOT NULL,
            gift_description TEXT NOT NULL,
            gift_type TEXT NOT NULL,
            photo_base64 TEXT NOT NULL,
            age_range TEXT NOT NULL,
            quality_score INTEGER,
            status TEXT DEFAULT 'available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_name TEXT NOT NULL,
            recipient_contact TEXT NOT NULL,
            recipient_address TEXT NOT NULL,
            child_age INTEGER,
            child_interests TEXT,
            specific_needs TEXT,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gift_id INTEGER,
            request_id INTEGER,
            match_score REAL,
            match_reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gift_id) REFERENCES gifts (id),
            FOREIGN KEY (request_id) REFERENCES requests (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def add_gift(gift_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gifts (donnor_name, donnor_contact, donor_address, gift_name, gift_description, gift_type, photo_base64, age_range, quality_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        gift_data['donnor_name'],
        gift_data['donnor_contact'],
        gift_data['donor_address'],
        gift_data['gift_name'],
        gift_data['gift_description'],
        gift_data['gift_type'],
        gift_data['photo_base64'],
        gift_data['age_range'],
        gift_data['quality_score']
    ))
    conn.commit()
    gift_id = cursor.lastrowid
    conn.close()
    return gift_id

def get_available_gifts():
    """Get all available gifts"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Returns dict-like rows
    c = conn.cursor()
    
    c.execute("SELECT * FROM gifts WHERE status = 'available' ORDER BY created_at DESC")
    gifts = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return gifts

def add_request(request_data):
    """Add a new request"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO requests
        (recipient_name, recipient_contact, recipient_location, 
         child_age, child_interests, specific_needs)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        request_data['recipient_name'],
        request_data['recipient_contact'],
        request_data['recipient_location'],
        request_data['child_age'],
        request_data['child_interests'],
        request_data['specific_needs']
    ))
    
    conn.commit()
    request_id = c.lastrowid
    conn.close()
    return request_id

def get_all_requests():
    """Get all open requests"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM requests WHERE status = 'open' ORDER BY created_at DESC")
    requests = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return requests

def claim_gift(gift_id, request_id):
    """Mark an gift as claimed"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Update gift status
    c.execute("UPDATE gifts SET status = 'claimed' WHERE id = ?", (gift_id,))
    
    # Create match record
    c.execute('''
        INSERT INTO matches (gift_id, request_id, status)
        VALUES (?, ?, 'accepted')
    ''', (gift_id, request_id))
    
    conn.commit()
    conn.close()

def get_stats():
    """Get dashboard statistics"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM gifts")
    total_gifts = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM gifts WHERE status = 'claimed'")
    claimed_gifts = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM requests")
    total_requests = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_gifts': total_gifts,
        'claimed_gifts': claimed_gifts,
        'total_requests': total_requests
    }

# Initialize database when module loads
initialize_db()

