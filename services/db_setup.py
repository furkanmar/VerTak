import sqlite3
import os
import config as c

def setup_database():
    # DB klasörü garanti olsun
    db_folder = os.path.dirname(c.DB_PATH)
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # Eğer zaten varsa, yeniden oluşturma
    if os.path.exists(c.DB_PATH):
        print("Veritabanı zaten mevcut.")
        return

    print("Veritabanı bulunamadı. Oluşturuluyor...")

    try:
        conn = sqlite3.connect(c.DB_PATH)
        cursor = conn.cursor()

        with open(c.SQL_PATH, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Veritabanı oluşturuldu.")
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        raise
