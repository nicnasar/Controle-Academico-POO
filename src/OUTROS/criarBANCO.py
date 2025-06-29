import sqlite3

class CriarBanco:
    def __init__(self, caminho_banco):
        self.caminho_banco = caminho_banco
        self._criar_banco()


    def _criar_banco(self):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS 
                Aluno (
                    nome INTEGER ,
                    cpf INTEGER UNIQUE,
                    idade TEXT,
                    email TEXT,
                    endereco TEXT
            )
        """)
        conexao.commit()