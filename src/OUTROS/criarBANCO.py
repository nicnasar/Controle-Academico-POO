import sqlite3

class CriarBanco:
    def __init__(self, db_path):
        self.db_path = db_path
        self._criar_banco()


    # ESTÁ ERRADO NÃO USAR
    def _criar_banco(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
            conn.commit()