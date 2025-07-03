import sqlite3
import requests
import json

from MODELOS.alunoMODELO import AlunoModelo


class AlunoDao:
    
    
    def __init__(self, caminho_banco): 
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo de uma vez
        self.caminho_banco = caminho_banco
    
    
    def inserir_aluno_dao(self, aluno: AlunoModelo):
        conexao = sqlite3.connect(self.caminho_banco) # abre o banco de dados
        cursor = conexao.cursor() # cria um cursor

        cursor.execute("SELECT * FROM Aluno WHERE cpf = ?", (aluno.cpf,))
        if cursor.fetchone():
            print("Aluno já cadastrado.")
            conexao.close()
            return False
    
        cursor.execute("""
                INSERT INTO
                Aluno (nome, cpf, idade, email, endereco)
                VALUES (?, ?, ?, ?, ?)
                """, 
                (
                        # cada valor corresponde a uma interrogação
                        aluno.nome, 
                        aluno.cpf, 
                        aluno.idade, 
                        aluno.email, 
                        aluno.endereco
                    )
            )
        conexao.commit() # fecha o banco de dados
        conexao.close()
        return True
    
    
    def atualizar_aluno_dao(self, aluno: AlunoModelo): # dentro de alunoDAO

        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM Aluno WHERE cpf = ?", (aluno.cpf,)) # mesma coisa pra verificar se tem aluno já cadastrado
        resultado = cursor.fetchone() # lembrando que fetch one, pega UMA linha, que nesse caso é uma tupla (?)

        if not resultado: # resultado recebe ou uma tupla ou None, None entra no if
            print("Aluno não encontrado.")
            conexao.close()
            return False

        # a tupla estará nessa ordem: resultado = ("nome", "cpf", idade, "email", "rua")

        if aluno.nome is not None:
            nome = aluno.nome
        else:
            nome = resultado[0]

        # abaixo tem essas quatro linhas de código compactada em uma linha só
        # nome = aluno.nome if aluno.nome is not None else resultado[0]
        # se for none, é porque não quis atualizar o nome, nesse casso, e mantém, logo pegou do banco de dados através de resultado[0]

        idade = aluno.idade if aluno.idade is not None else resultado[2]
        email = aluno.email if aluno.email is not None else resultado[3]
        endereco = aluno.endereco if aluno.endereco is not None else resultado[4]

        cursor.execute("""
            UPDATE Aluno SET nome = ?, idade = ?, email = ?, endereco = ?
            WHERE cpf = ?
        """, (nome, idade, email, endereco, aluno.cpf))

        conexao.commit()
        conexao.close()
        return True


    def deletar_aluno_dao(self, aluno: AlunoModelo):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM Aluno WHERE cpf = ?", (aluno.cpf,)) 
        if not cursor.fetchone():
            conexao.close()
            return False

        cursor.execute("DELETE FROM Aluno WHERE cpf = ?", (aluno.cpf,))
        conexao.commit()
        conexao.close()
        return True
    
    



