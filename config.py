import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data/vertak.db')
SQL_PATH = os.path.join(BASE_DIR, 'data/init_db.sql')