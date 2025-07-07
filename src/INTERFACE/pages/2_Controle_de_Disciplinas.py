# Barbára Lima
# Nicolas Nasário
# Victória Kallas

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from MODELOS.disciplinasMODELO import DisciplinaModelo
from DAO.disciplinasDAO import DisciplinaDao
from CONTROLE.controleDISCIPLINAS import ControleDisciplina

st.set_page_config(
    page_title="Controle de Disciplinas",
    layout="wide"
)

class ControleDisciplinasPage:
    """Classe responsável pela interface de controle de disciplinas"""
    
    def __init__(self, nome_banco):
        self.nome_banco = nome_banco
        self.controlador = ControleDisciplina(DisciplinaDao(nome_banco))
        self._init_session()
    
    def _init_session(self):
        """Inicializa variáveis de sessão"""
        defaults = {
            'sucesso_disciplina': None,
            'codigo_atualizado': None,
            'codigo_deletado': None
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def exibir_feedback(self):
        """Exibe mensagens de feedback"""
        if st.session_state.sucesso_disciplina:
            msgs = {
                "cadastro": "Disciplina cadastrada com sucesso!",
                "atualizacao": f"Disciplina código {st.session_state.codigo_atualizado} atualizada!",
                "delecao": f"Disciplina código {st.session_state.codigo_deletado} removida!"
            }
            st.success(msgs[st.session_state.sucesso_disciplina])

            for key in ['sucesso_disciplina', 'codigo_atualizado', 'codigo_deletado']:
                st.session_state[key] = None
    
    def listar_disciplinas(self):
        """Lista todas as disciplinas"""
        st.subheader("Lista de Disciplinas Cadastradas")
        disciplinas = self.controlador.listar_todas_disciplinas()
        
        if disciplinas:
            df = pd.DataFrame(disciplinas, columns=["Código", "Nome", "Carga Horária", "Professor"])
            st.dataframe(df, use_container_width=True)
            st.info(f"Total: {len(disciplinas)} disciplinas")
        else:
            st.warning("Nenhuma disciplina cadastrada.")
    
    def cadastrar_disciplina(self):
        """Formulário para cadastrar disciplina"""
        st.subheader("Cadastrar Nova Disciplina")
        
        with st.form("form_cadastrar_disciplina"):
            col1, col2 = st.columns(2)
            
            with col1:
                codigo = st.number_input("Código *", min_value=1, step=1)
                nome = st.text_input("Nome", placeholder="Ex: Cálculo I")
            
            with col2:
                carga_horaria = st.number_input("Carga Horária", min_value=0, step=1, value=0)
                nome_professor = st.text_input("Professor", placeholder="Ex: Dr. Silva")
            
            if st.form_submit_button("Cadastrar", type="primary"):
                try:
                    if self.controlador.buscar_disciplina_por_codigo(codigo):
                        return st.error("Código já cadastrado!")
                    
                    disciplina = DisciplinaModelo(
                        codigo, 
                        nome if nome else None, 
                        carga_horaria if carga_horaria > 0 else None, 
                        nome_professor if nome_professor else None
                    )
                    
                    if self.controlador.cadastrar_disciplina(disciplina):
                        st.session_state.sucesso_disciplina = "cadastro"
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar.")
                except Exception as e:
                    st.error(f"Erro: {e}")
    
    def atualizar_disciplina(self):
        """Formulário para atualizar disciplina"""
        st.subheader("Atualizar Disciplina")
        codigo_busca = st.number_input("Código da disciplina:", min_value=0, step=1, value=0)
        
        if codigo_busca > 0:
            try:
                disciplina = self.controlador.buscar_disciplina_por_codigo(codigo_busca)
                
                if disciplina:
                    st.success(f"Encontrada: {disciplina[1] or 'Sem nome'}")
                    with st.form(f"update_{codigo_busca}_{hash(str(disciplina))}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nome = st.text_input("Nome", value=disciplina[1] or "")
                            carga = st.number_input("Carga Horária", min_value=0, value=disciplina[2] or 0)
                        
                        with col2:
                            professor = st.text_input("Professor", value=disciplina[3] or "")
                        
                        if st.form_submit_button("Atualizar", type="primary"):
                            disciplina_nova = DisciplinaModelo(
                                codigo_busca,
                                nome if nome else None,
                                carga if carga > 0 else None,
                                professor if professor else None
                            )
                            
                            if self.controlador.atualizar_disciplina(disciplina_nova):
                                st.session_state.sucesso_disciplina = "atualizacao"
                                st.session_state.codigo_atualizado = codigo_busca
                                st.rerun()
                            else:
                                st.error("Erro ao atualizar.")
                else:
                    st.error("Disciplina não encontrada.")
            except Exception as e:
                st.error(f"Erro: {e}")
    
    def deletar_disciplina(self):
        """Formulário para deletar disciplina"""
        st.subheader("Remover Disciplina")
        st.warning("Ação irreversível!")
        codigo_del = st.number_input("Código para remoção:", min_value=0, step=1, value=0, key="del_codigo")
        
        if codigo_del > 0:
            try:
                disciplina = self.controlador.buscar_disciplina_por_codigo(codigo_del)
                
                if disciplina:
                    st.info(f"**{disciplina[1] or 'Sem nome'}** - Código: {disciplina[0]}")
                    
                    if st.checkbox("Confirmar remoção", key=f"conf_{codigo_del}"):
                        if st.button("Remover", type="secondary", key=f"del_{codigo_del}"):
                            disciplina_del = DisciplinaModelo(codigo_del, None, None, None)
                            if self.controlador.deletar_disciplina(disciplina_del):
                                st.session_state.sucesso_disciplina = "delecao"
                                st.session_state.codigo_deletado = codigo_del
                                st.rerun()
                            else:
                                st.error("Erro ao remover.")
                else:
                    st.error("Disciplina não encontrada.")
            except Exception as e:
                st.error(f"Erro: {e}")

def main():
    st.title("Gestão de Disciplinas")
    
    nome_banco = "controle_academico.db"
    pagina = ControleDisciplinasPage(nome_banco)
    
    pagina.exibir_feedback()
    
    operacao = st.selectbox("Operação:", 
                           ["Listar Disciplinas", "Cadastrar Disciplina", "Atualizar Disciplina", "Deletar Disciplina"])
    
    operations = {
        "Listar Disciplinas": pagina.listar_disciplinas,
        "Cadastrar Disciplina": pagina.cadastrar_disciplina,
        "Atualizar Disciplina": pagina.atualizar_disciplina,
        "Deletar Disciplina": pagina.deletar_disciplina
    }
    operations[operacao]()

if __name__ == "__main__":
    main()