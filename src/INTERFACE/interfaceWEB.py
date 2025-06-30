# não permitir que nada seja cadastrado caso algum item esteja em branco

# formatar dados de entrada. Ex.: <int> 1326402714 --> <str> "132.634.027-14", datas e hora também

# APENAS fazer isso no DISPLAY. No banco os dados devem estar crus

# criar funções para dar display nos dados de forma correta

# caso der erro ao cadastrar qualquer coisa, os dados devem permanecer na tela. Do contrário, eles devem ser apagados dos espaços


"""
    LIMITAÇÕES DA INTERFACE COM BASE NO BANCO DE DADOS:
        Disciplina:
        - codigo: deve ser INTEIRO, não recber nada além disso
        - nome: pode ser STRING ou NONE
        - carga_horaria: pode ser INTEIRO ou NONE
        - nome_professor: pode ser STRING ou NONE
        
        Aluno:
        - nome: STRING, não receber nada além disso
        - cpf: INTEIRO, não receber nada além disso
        - idade: INTEIRO, não receber nada além disso
        - email: STRING, não receber nada além disso
        - endereço: STRING, não receber nada além disso
        
        Matricula:
        - codigo_disciplina: INTEIRO APENAS
        - cpf_aluno: INTEIRO APENAS
        - data_matricula: converter para STRING
        - horario matricula: converter para STRING
"""


import streamlit as st

st.title("Minha Interface Simples")

valor = st.number_input(label="Digite um numero: ", min_value=0) # inteiro

if st.button("Enter"):
    print(valor, type(valor))
    st.success("Valor enviado! Veja o terminal.")

    
