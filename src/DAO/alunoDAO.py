import sqlite3

from MODELOS.alunoMODELO import AlunoModelo

class AlunoDao:
    def inserir_aluno(self, aluno: AlunoModelo):
        conn = sqlite3.connect("..controle_academico.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO"
            "Aluno (nome, cpf, idade, email, endereco)"
            "VALUES (?, ?, ?, ?, ?)", 
                (
                    # cada valor corresponde a uma interrogação
                    aluno.nome, 
                    aluno.CPF, 
                    aluno.idade, 
                    aluno.email, 
                    aluno.endereco)
            )
        conn.commit()
    




