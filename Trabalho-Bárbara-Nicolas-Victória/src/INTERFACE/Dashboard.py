# Barbára Lima
# Nicolas Nasário
# Victória Kallas

import streamlit as st
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from OUTROS.criarBANCO import CriarBanco
from DAO.alunoDAO import AlunoDao
from CONTROLE.controleALUNOS import ControleAluno
from DAO.disciplinasDAO import DisciplinaDao
from CONTROLE.controleDISCIPLINAS import ControleDisciplina
from DAO.matriculasDAO import MatriculaDao
from CONTROLE.controleMATRICULAS import ControleMatricula

nome_banco = "controle_academico.db"

banco = CriarBanco(nome_banco)


st.set_page_config(
    page_title="Sistema de Controle Acadêmico",
    layout="wide"
)

def main():
    
    st.title("Sistema de Controle Acadêmico")
    st.markdown("**Bem-vindo ao sistema de gestão acadêmica**")
    
if __name__ == "__main__":
    main()