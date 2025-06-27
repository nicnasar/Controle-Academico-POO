import streamlit as st
from controle.controle_disciplinas import pagina_controle_disciplinas
import database.banco_de_dados as database

def main():
    db = database.BancoDeDados()
    db.criar_banco()
    st.sidebar.title("Menu")
    opcao = st.sidebar.selectbox("Escolha uma opção:", ["Controle de Disciplinas"])
    if opcao == "Controle de Disciplinas":
        pagina_controle_disciplinas()

if __name__ == "__main__":
    main()

