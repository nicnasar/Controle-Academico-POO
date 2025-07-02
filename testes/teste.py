# teste2
'''import requests
import json

resposta = requests.get('https://viacep.com.br/ws/29070220/json/').text

dados = json.loads(resposta)

print(dados)
print('Endereço',dados['logradouro'])'''

# teste3

'''import requests
import json



def validar_CEP(cep):

    # cep = input(('Digite o seu CEP (sem pontuações): '))

    if len(str(cep)) != 8:
        print('CEP inválido.')

        return False 

    link = f'https://viacep.com.br/ws/{cep}/json/'

    resposta = requests.get(link).text

    dados = json.loads(resposta)

    if dados['logradouro'] == '':
        dados['logradouro'] = input(str('Digite o sua rua:'))
        
    if dados['bairro'] == '':
        dados['bairro'] = input(str('Digite o seu bairro: '))
        
    if dados['localidade'] == '':
        dados['localidade'] = input(str('Digite a sua cidade: '))
        
    if dados['estado'] == '':
        dados['estado'] = input(str('Digite o seu estado: '))

    print(dados)

    return f'{dados['logradouro']}, {dados['cep']}, {dados['bairro']}, {dados['localidade']}, {dados['estado']}'

print(validar_CEP(95555000))'''
# Exemplo de CEP que não tem logradouro registrado para teste 95555000
"""
Preciso verificar se o cep retorna um endereço

"""
# teste 04 função de atualizar aluno

import sqlite3
import sys
import os
sys.path.append(os.path.abspath(".."))

from MODELOS.alunoMODELO import AlunoModelo

sys.path.append(os.path.abspath(".."))

def atualizar_aluno(self, aluno: AlunoModelo): # dentro de alunoDAO

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


# teste 05

'''def deletar_aluno(self, cpf):
    conexao = sqlite3.connect(self.caminho_banco)
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM Aluno WHERE cpf = ?", (cpf,)) 
    if not cursor.fetchone():
        print("Aluno não encontrado no banco de dados!")
        conexao.close()
        return False

    cursor.execute("DELETE FROM Aluno WHERE cpf = ?", (cpf,))
    conexao.commit()
    conexao.close()
    print("Aluno removido com sucesso!")
    return True
'''

