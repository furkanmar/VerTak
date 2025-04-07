-- Kullanıcı tablosu
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    creation_time TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Şirket tablosu
CREATE TABLE IF NOT EXISTS company (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    tax_no TEXT,
    company_representer TEXT,
    credit_amount REAL NOT NULL DEFAULT 0,
    debit_amount REAL NOT NULL DEFAULT 0,
    net_amount REAL NOT NULL DEFAULT 0,
    number_of_transaction NOT NULL DEFAULT 0,
    creation_time TEXT NOT NULL DEFAULT (datetime('now'))
);

-- İşlem tablosu
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    explanation TEXT,
    transaction_date TEXT NOT NULL DEFAULT (datetime('now')),
    credit_amount REAL NOT NULL,
    debit_amount REAL NOT NULL,
    current_balance REAL NOT NULL DEFAULT 0,
    paymet_type TEXT,
    bill BLOB,
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);

-- Kullanıcı ekle (eğer yoksa)
INSERT INTO user (username, password, creation_time)
SELECT 'admin', '123', datetime('now')
WHERE NOT EXISTS (
    SELECT 1 FROM user WHERE username = 'admin'
);


