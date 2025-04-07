import sqlite3
import config as c


def setup_database():
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    
    # SQL'i çalıştır ve veritabanını yarat
    with open(c.SQL_PATH, 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()