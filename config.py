import os
import sys

# 1. Salt veri dosyaları (SQL, poppler) için konum
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # exe içindeki unpack edilen geçici dizin
    EXEC_DIR = os.path.dirname(sys.executable)  # exe'nin bulunduğu gerçek dizin
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXEC_DIR = BASE_DIR

# 2. Kalıcı yazılabilir veritabanı (ProgramData)
PROGRAM_DATA = os.environ.get("PROGRAMDATA", "C:\\ProgramData")
APP_DATA_DIR = os.path.join(PROGRAM_DATA, "VERTAK")
os.makedirs(APP_DATA_DIR, exist_ok=True)

# 3. Yol tanımları
DB_PATH = os.path.join(APP_DATA_DIR, "vertak.db")  # yazılabilir klasör
SQL_PATH = os.path.join(BASE_DIR, "data", "init_db.sql")

LOGO_PATH = os.path.join(BASE_DIR,"logo.png")

def get_poppler_path():
    if getattr(sys, 'frozen', False):  # Eğer .exe olarak çalışıyorsa
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "resources", "poppler", "bin")