import sqlite3
from datetime import datetime
class Account:
    def __init__(self, account, balance, transfed):
        self.account = account
        self.balance = balance
        self.transfed = transfed

class HXAccount:
    def __init__(self,type,account, password):
        self.type = type
        self.account = account
        self.password = password
class Database:
    def __init__(self, db_file):
        current_date = datetime.now()
        day = current_date.strftime("%Y-%m-%d")
        self.conn = sqlite3.connect(day+"_"+db_file)
        # self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account TEXT PRIMARY KEY,
                balance REAL,
                transfed BOOLEAN
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hx_accounts(
                type INTEGER PRIMARY KEY,
                account TEXT NOT NULL UNIQUE,
                password TEXT)
        ''')
        self.conn.commit()
    def get_all_accounts(self):
        self.cursor.execute('SELECT * FROM accounts WHERE transfed = 0 ORDER BY account ASC')
        rows = self.cursor.fetchall()
        accounts = [Account(*row) for row in rows]
        return accounts
    def clear_table(self):
        self.cursor.execute('DELETE FROM accounts')
        self.conn.commit()

    def insert_account(self, account, balance, transfed):
        self.cursor.execute('''
            INSERT OR REPLACE INTO accounts (account, balance, transfed)
            VALUES (?, ?, ?)
        ''', (account, balance, transfed))
        self.conn.commit()
    def insert_hx_account(self, account, password):
        self.cursor.execute('''
            INSERT OR REPLACE INTO hx_accounts (account, type, password)
            VALUES (?, ?, ?)
        ''', (account, 1, password))
        self.conn.commit()
    def get_hx_account(self):
        self.cursor.execute('SELECT * FROM hx_accounts WHERE type = 1')
        row = self.cursor.fetchone()
        if row:
            return HXAccount(*row)
        return None

    def get_account(self, account):
        self.cursor.execute('SELECT * FROM accounts WHERE account = ?', (account,))
        row = self.cursor.fetchone()
        if row:
            return Account(*row)
        return None

    def get_account_by_transfed(self, transfed):
        self.cursor.execute('SELECT * FROM accounts WHERE transfed = ?  ORDER BY account ASC', (transfed,))
        rows = self.cursor.fetchall()
        accounts = [Account(*row) for row in rows]
        return accounts
# if __name__ == '__main__':
#     db = Database('accounts.db')
#     db.insert_account('test_account1', 100, False)
#     account=db.get_account('test_account1')
#     print(account.account)
#     db.insert_hx_account('test_account', 'test_password')
#     hx_account=db.get_hx_account()
#     print(hx_account.account)