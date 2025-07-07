# Barbára Lima

import streamlit as st

from DAO.alunoDAO import AlunoDao
from CONTROLE.controleALUNOS import ControleAluno
from DAO.disciplinasDAO import DisciplinaDao
from CONTROLE.controleDISCIPLINAS import ControleDisciplina
from DAO.matriculasDAO import MatriculaDao
from CONTROLE.controleMATRICULAS import ControleMatricula

st.set_page_config(
    page_title="Sistema de Controle Acadêmico",
    layout="wide"
)

def main():
    
    st.title("Sistema de Controle Acadêmico")
    st.markdown("**Bem-vindo ao sistema de gestão acadêmica**")
    
if __name__ == "__main__":
    main()