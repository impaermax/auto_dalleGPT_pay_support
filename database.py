import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bot_db.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            username TEXT,
                            balance INTEGER DEFAULT 3,
                            is_approved INTEGER DEFAULT 0)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            amount INTEGER,
                            status TEXT DEFAULT 'pending')''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS support_tickets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            message TEXT,
                            status TEXT DEFAULT 'open')''')
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()

    def add_user(self, user_id, username):
        self.cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        self.conn.commit()

    def update_balance(self, user_id, delta):
        self.cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (delta, user_id))
        self.conn.commit()

    def add_support_ticket(self, user_id, message):
        self.cursor.execute('INSERT INTO support_tickets (user_id, message) VALUES (?, ?)', (user_id, message))
        self.conn.commit()
