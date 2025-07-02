import sqlite3
import requests
import json

from MODELOS.alunoMODELO import AlunoModelo


class AlunoDao:
    
    
    def __init__(self, caminho_banco): 
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo de uma vez
        self.caminho_banco = caminho_banco
    
    
    def inserir_aluno(self, aluno: AlunoModelo):
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
    
    def listar_alunos(self):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, cpf, idade, email, endereco FROM Aluno")
        alunos = cursor.fetchall()
        conexao.close()
        return alunos
    
    def validar_CEP(self,cep):

        if len(str(cep)) != 8:
            print('CEP inválido.')

            return False 

        link = f'https://viacep.com.br/ws/{cep}/json/'

        resposta = requests.get(link).text

        dados = json.loads(resposta)

        if dados['logradouro'] == '':
            dados['logradouro'] = input(str('Digite a sua rua:'))
            
        if dados['bairro'] == '':
            dados['bairro'] = input(str('Digite o seu bairro: '))
            
        if dados['localidade'] == '':
            dados['localidade'] = input(str('Digite a sua cidade: '))
            
        if dados['estado'] == '':
            dados['estado'] = input(str('Digite o seu estado: '))

        print(dados)

        return f'{dados['logradouro']}, {dados['cep']}, {dados['bairro']}, {dados['localidade']}, {dados['estado']}'
            



