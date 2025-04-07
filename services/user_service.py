import sqlite3
import datetime, os
import config as c

def check_log_info(username, password):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username FROM user WHERE username = ? AND password = ?
    ''', (username, password))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None
