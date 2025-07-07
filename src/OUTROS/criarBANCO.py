# Barbára Lima
# Nicolas Nasário
# Victória Kallas

import sqlite3

# com base em https://www.sqlitetutorial.net/sqlite-python/creating-tables/

tabelas_sqlite = [
    """CREATE TABLE IF NOT EXISTS 
        Disciplina (
            codigo INTEGER UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            carga_horaria INTEGER NOT NULL,
            nome_professor TEXT NOT NULL
        );""",
        
    """CREATE TABLE IF NOT EXISTS
        Aluno (
            nome TEXT NOT NULL,
            cpf INTEGER NOT NULL UNIQUE,
            idade INTEGER NOT NULL,
            email TEXT NOT NULL,
            endereco TEXT NOT NULL
        );""",
        
    """CREATE TABLE IF NOT EXISTS
        Matricula (
            codigo_disciplina INTEGER NOT NULL,
            cpf_aluno INTEGER NOT NULL,
            data_matricula TEXT NOT NULL, 
            horario_matricula TEXT NOT NULL
        );"""
]


class CriarBanco:
    def __init__(self, caminho_banco):
        self.caminho_banco = caminho_banco
        self._criar_banco()


    def _criar_banco(self):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        # cria cada uma das tabelas contidas na lista
        for tabela in tabelas_sqlite:        
            cursor.execute(tabela)
            
        conexao.commit()