import sqlite3
import datetime, os
import config as c


def get_all_company():
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT company_id, company_name, credit_amount, debit_amount, net_amount, number_of_transaction FROM company" 
    )
    companies = cursor.fetchall()
    conn.close()
    return companies


def calculate_amounts():
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(credit_amount) FROM company")
    total_credit = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(debit_amount) FROM company")
    total_debit = cursor.fetchone()[0] or 0

    conn.close()

    net_balance = total_credit - total_debit

    amounts = {
        "total_credit": total_credit,
        "total_debit": total_debit,
        "net_balance": net_balance
    }
    return amounts


def get_company(company_id):

    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM compony WHERE company_id = ? ",
        (company_id)
    )
    company = cursor.fetchone()
    conn.close()
    return company

def create_company(name, tax_no=None, representer=None):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO company (
            company_name, tax_no, company_representer,
            credit_amount, debit_amount, net_amount,
            number_of_transaction, creation_time
        )
        SELECT ?, ?, ?, 0, 0, 0, 0, datetime('now')
        WHERE NOT EXISTS (
            SELECT 1 FROM company WHERE company_name = ?
        )
    """, (name, tax_no, representer, name))

    conn.commit()
    inserted = cursor.rowcount  # 0 ise eklenmedi
    conn.close()
    return inserted

def get_company_by_id(company_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, tax_no, company_representer
        FROM company
        WHERE company_id = ?
    """, (company_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'company_name': row[0],
            'tax_no': row[1],
            'company_representer': row[2]
        }
    return None

def update_company(company_id, name, tax_no=None, representer=None):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE company
        SET company_name = ?, tax_no = ?, company_representer = ?
        WHERE company_id = ?
    """, (name, tax_no, representer, company_id))
    conn.commit()
    conn.close()

def delete_company(company_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM company WHERE company_id = ?", (company_id,))
    conn.commit()
    conn.close()

def recalculate_company_balance(company_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            IFNULL(SUM(credit_amount), 0),
            IFNULL(SUM(debit_amount), 0)
        FROM transactions
        WHERE company_id = ?
    """, (company_id,))
    
    total_credit, total_debit = cursor.fetchone()
    net_amount = total_credit - total_debit

    cursor.execute("""
        UPDATE company
        SET credit_amount = ?, debit_amount = ?, net_amount = ?
        WHERE company_id = ?
    """, (total_credit, total_debit, net_amount, company_id))

    conn.commit()
    conn.close()