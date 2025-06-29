import sqlite3

from MODELOS.alunoMODELO import AlunoModelo

class AlunoDao:
    
    
    def __init__(self, caminho_banco): 
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo de uma vez
        self.caminho_banco = caminho_banco
    
    
    
    def inserir_aluno(self, aluno: AlunoModelo):
        conexao = sqlite3.connect(self.caminho_banco) # abre o banco de dados
        cursor = conexao.cursor() # cria um cursor
        cursor.execute("""
                INSERT INTO
                Aluno (nome, cpf, idade, email, endereco)
                VALUES (?, ?, ?, ?, ?)
                """, 
                (
                        # cada valor corresponde a uma interrogação
                        aluno.nome, 
                        aluno.CPF, 
                        aluno.idade, 
                        aluno.email, 
                        aluno.endereco
                    )
            )
        conexao.commit() # fecha o banco de dados
    
    
    def listar_alunos(self):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, cpf, idade, email, endereco FROM Aluno")
        alunos = cursor.fetchall()
        conexao.close()
        return alunos
    




