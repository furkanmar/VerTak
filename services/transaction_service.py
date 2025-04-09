import sqlite3
import datetime, os
import config as c
from services.company_service import recalculate_company_balance


def get_all_transaction(company_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT transaction_id, transaction_date, explanation, credit_amount, debit_amount, current_balance, paymet_type,bill_added_date, bill
        FROM transactions
        WHERE company_id = ?
        ORDER BY transaction_date ASC, transaction_id ASC
    """, (company_id,))
    
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_bill_by_id(transaction_id):
    conn = sqlite3.connect(c.DB_PATH) 
    cursor = conn.cursor()

    cursor.execute("SELECT bill FROM transactions WHERE transaction_id = ?", (transaction_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # bytes
    return None

def calculate_amounts(company_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(credit_amount) FROM transactions where company_id =? ",(company_id))
    total_credit = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(debit_amount) FROM transactions where company_id =? ",(company_id))
    total_debit = cursor.fetchone()[0] or 0

    conn.close()

    net_balance = total_credit - total_debit

    amounts = {
        "total_credit": total_credit,
        "total_debit": total_debit,
        "net_balance": net_balance
    }
    return amounts

def add_transaction(company_id, date, explanation, credit, debit, payment_type, bill_added_date=None,bill=None):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (
            company_id,
            explanation,
            transaction_date,
            credit_amount,
            debit_amount,
            paymet_type,
            bill_added_date,
            bill
        )
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
    """, (company_id, explanation, date, credit, debit, payment_type,bill_added_date, bill))

    conn.commit()
    conn.close()

    # Tüm balance'ları yeniden hesapla
    recalculate_company_balance(company_id)
    recalculate_balances(company_id)

def recalculate_balances(company_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    # Tüm işlemleri sırayla al (önce tarih, sonra id)
    cursor.execute("""
        SELECT transaction_id, credit_amount, debit_amount
        FROM transactions
        WHERE company_id = ?
        ORDER BY transaction_date ASC, transaction_id ASC
    """, (company_id,))
    
    transactions = cursor.fetchall()

    balance = 0
    for trans_id, credit, debit in transactions:
        balance += credit - debit
        cursor.execute("""
            UPDATE transactions
            SET current_balance = ?
            WHERE transaction_id = ?
        """, (balance, trans_id))

    conn.commit()
    conn.close()


def update_transaction(transaction_id, data):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET explanation = ?, credit_amount = ?, debit_amount = ?, paymet_type = ?, bill_added_date = ? ,bill = ?
        WHERE transaction_id = ?
    """, (
        data["explanation"],
        data["credit"],
        data["debit"],
        data["payment_type"],
        data["bill_added_date"],
        data["bill"],
        transaction_id
    ))

    # İlgili şirketin id'sini bulup bakiyesini güncelle
    cursor.execute("SELECT company_id FROM transactions WHERE transaction_id = ?", (transaction_id,))
    row = cursor.fetchone()
    if row:
        company_id = row[0]
        conn.commit()
        conn.close()
        recalculate_company_balance(company_id)
        recalculate_balances(company_id)

def get_transaction_by_id(transaction_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT explanation, credit_amount, debit_amount, paymet_type, bill
        FROM transactions
        WHERE transaction_id = ?
    """, (transaction_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "explanation": row[0],
            "credit": row[1],
            "debit": row[2],
            "payment_type": row[3],
            "bill": row[4]
        }
    return None

def delete_transaction(transaction_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    # Şirket ID'sini bul
    cursor.execute("SELECT company_id FROM transactions WHERE transaction_id = ?", (transaction_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return  # işlem yoksa çık

    company_id = row[0]

    # Silme işlemi
    cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    recalculate_balances(company_id)
    recalculate_company_balance(company_id)
