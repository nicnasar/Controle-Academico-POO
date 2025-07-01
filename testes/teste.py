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

    #cep = input(('Digite o seu CEP (sem pontuações): '))

    link = f'https://viacep.com.br/ws/{cep}/json/'

    resposta = requests.get(link).text

    dados = json.loads(resposta)

    print(dados)
    # print('Endereço',dados['logradouro'])

    return f'{dados['logradouro']},{dados['cep']},{dados['bairro']}, {dados['localidade']},{dados['estado']}'


print(validar_CEP(29070220))
