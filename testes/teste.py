# teste2
'''import requests
import json

resposta = requests.get('https://viacep.com.br/ws/29070220/json/').text

dados = json.loads(resposta)

print(dados)
print('Endereço',dados['logradouro'])'''

# teste3

import requests
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
    # print('Endereço',dados['logradouro'])

    return f'{dados['logradouro']},{dados['cep']},{dados['bairro']}, {dados['localidade']},{dados['estado']}'

print(validar_CEP(95555000))
# Exemplo de CEP que não tem logradouro registrado para teste 95555000
"""
Preciso verificar se o cep retorna um endereço

"""