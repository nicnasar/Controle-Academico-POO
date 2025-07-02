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
        logradouro = input(str('Digite o seu endereço:'))
    if dados['bairro'] == '':
        bairro = input(str('Digite'))

    print(dados)
    # print('Endereço',dados['logradouro'])

    return f'{dados['logradouro']},{dados['cep']},{dados['bairro']}, {dados['localidade']},{dados['estado']}'

print(validar_CEP(29070220))

"""
Preciso verificar se o cep retorna um endereço

"""