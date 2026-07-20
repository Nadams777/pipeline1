"""Database query functions"""
import sqlite3

def get_user_by_id(user_id):
    """Fetch user from database - VULNERABLE TO SQL INJECTION"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SQL Injection vulnerability: string concatenation
    query = "SELECT * FROM users WHERE id=" + str(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    
    conn.close()
    return result

def search_users(search_term):
    """Search users - VULNERABLE TO SQL INJECTION"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Another SQL injection vulnerability
    query = f"SELECT * FROM users WHERE email LIKE '%{search_term}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results
