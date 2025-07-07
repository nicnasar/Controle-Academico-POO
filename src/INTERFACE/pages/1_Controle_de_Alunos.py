# Barbára Lima
# Nicolas Nasário
# Victória Kallas

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from MODELOS.alunoMODELO import AlunoModelo
from DAO.alunoDAO import AlunoDao
from CONTROLE.controleALUNOS import ControleAluno
from VALIDACOES.validacoesALUNO import ValidarAluno

st.set_page_config(
    page_title="Controle de Alunos",
    layout="wide"
)

class ControleAlunosPage:
    """Classe responsável pela interface de controle de alunos"""
    
    def __init__(self, nome_banco):
        self.nome_banco = nome_banco
        self.controlador = ControleAluno(AlunoDao(nome_banco))
        self.validador = ValidarAluno(nome_banco)
        self._init_session()
    
    def _init_session(self):
        """Inicializa variáveis de sessão"""
        defaults = {
            'sucesso_aluno': None,
            'cpf_atualizado': None,
            'cpf_deletado': None,
            'nome_deletado': None,
            'endereco_auto': "",
            'cep_atual': ""
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def formatar_cpf(self, cpf):
        """Formata CPF para XXX.XXX.XXX-XX"""
        cpf_str = str(cpf).zfill(11)
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"

    def exibir_feedback(self):
        """Exibe mensagens de feedback"""
        if st.session_state.sucesso_aluno:
            msgs = {
                "cadastro": "Aluno cadastrado com sucesso!",
                "atualizacao": f"Aluno CPF {self.formatar_cpf(st.session_state.cpf_atualizado)} atualizado!",
                "delecao": f"Aluno {st.session_state.nome_deletado} (CPF: {self.formatar_cpf(st.session_state.cpf_deletado)}) removido!"
            }
            st.success(msgs[st.session_state.sucesso_aluno])

            for key in ['sucesso_aluno', 'cpf_atualizado', 'cpf_deletado', 'nome_deletado']:
                st.session_state[key] = None
    
    def listar_alunos(self):
        """Lista todos os alunos"""
        st.subheader("Lista de Alunos Cadastrados")
        alunos = self.controlador.listar_todos_alunos()
        
        if alunos:
            df = pd.DataFrame(alunos, columns=["Nome", "CPF", "Idade", "Email", "Endereço"])
            df["CPF"] = df["CPF"].apply(self.formatar_cpf)
            st.dataframe(df, use_container_width=True)
            st.info(f"Total: {len(alunos)} alunos")
        else:
            st.warning("Nenhum aluno cadastrado.")
    
    def cadastrar_aluno(self):
        """Formulário para cadastrar aluno"""
        st.subheader("Cadastrar Novo Aluno")
        
        with st.form("form_cadastrar_aluno", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome *", placeholder="João Silva")
                cpf = st.text_input("CPF *", placeholder="12345678901", max_chars=11)
                idade = st.number_input("Idade *", 1, 120, 18)
            
            with col2:
                email = st.text_input("Email *", placeholder="joao@email.com")
                cep = st.text_input("CEP", placeholder="12345678", max_chars=8)
                
                if cep != st.session_state.cep_atual:
                    st.session_state.cep_atual = cep
                    
                    if cep and len(cep) == 8 and cep.isdigit():
                        try:
                            endereco_cep = self.validador.validar_CEP(cep)
                            if endereco_cep:
                                st.session_state.endereco_auto = endereco_cep
                                st.success("CEP encontrado!")
                            else:
                                st.session_state.endereco_auto = ""
                                st.warning("CEP não encontrado.")
                        except:
                            st.session_state.endereco_auto = ""
                    elif not cep:
                        st.session_state.endereco_auto = ""
                
                endereco = st.text_area("Endereço *", value=st.session_state.endereco_auto)
            
            if st.form_submit_button("Cadastrar", type="primary"):
                if not all([nome, cpf, email, endereco]):
                    return st.error("Preencha todos os campos obrigatórios.")
                
                if len(cpf) != 11 or not cpf.isdigit():
                    return st.error("CPF deve ter 11 dígitos.")
                
                if "@" not in email:
                    return st.error("Email inválido.")
                
                try:
                    cpf_int = int(cpf)
                    
                    if self.validador.cpf_igual(cpf_int):
                        return st.error("CPF já cadastrado!")
                    
                    aluno = AlunoModelo(nome, cpf_int, idade, email, endereco)
                    
                    if self.controlador.cadastrar_aluno(aluno):
                        st.session_state.sucesso_aluno = "cadastro"
                        st.session_state.endereco_auto = ""
                        st.session_state.cep_atual = ""
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar.")
                except Exception as e:
                    st.error(f"Erro: {e}")
    
    def atualizar_aluno(self):
        """Formulário para atualizar aluno"""
        st.subheader("Atualizar Dados do Aluno")
        cpf_busca = st.text_input("CPF do aluno:", max_chars=11)
        
        if cpf_busca and len(cpf_busca) == 11 and cpf_busca.isdigit():
            try:
                cpf_int = int(cpf_busca)
                aluno = self.controlador.buscar_aluno_por_cpf(cpf_int)
                
                if aluno:
                    st.success(f"Aluno encontrado: {aluno[0]}")
                    
                    with st.form(f"update_aluno_{cpf_busca}_{hash(str(aluno))}", clear_on_submit=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nome = st.text_input("Nome", value=aluno[0])
                            idade = st.number_input("Idade", 1, 120, value=aluno[2])
                        
                        with col2:
                            email = st.text_input("Email", value=aluno[3])
                            endereco = st.text_area("Endereço", value=aluno[4])
                        
                        if st.form_submit_button("Atualizar", type="primary"):
                            if all([nome, email, endereco]):
                                aluno_novo = AlunoModelo(nome, cpf_int, idade, email, endereco)
                                if self.controlador.atualizar_aluno(aluno_novo):
                                    st.session_state.sucesso_aluno = "atualizacao"
                                    st.session_state.cpf_atualizado = cpf_int
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar.")
                            else:
                                st.error("Preencha todos os campos.")
                else:
                    st.error("Aluno não encontrado.")
            except Exception as e:
                st.error(f"Erro: {e}")
    
    def deletar_aluno(self):
        """Formulário para deletar aluno"""
        st.subheader("Remover Aluno do Sistema")
        st.warning("Ação irreversível!")
        cpf_del = st.text_input("CPF para remoção:", max_chars=11, key="del_cpf_aluno")
        
        if cpf_del and len(cpf_del) == 11 and cpf_del.isdigit():
            try:
                cpf_int = int(cpf_del)
                aluno = self.controlador.buscar_aluno_por_cpf(cpf_int)
                
                if aluno:
                    st.info(f"**{aluno[0]}** - CPF: {self.formatar_cpf(cpf_int)}")
                    
                    if st.checkbox("Confirmar remoção", key=f"conf_aluno_{cpf_del}"):
                        if st.button("Remover", type="secondary", key=f"del_aluno_{cpf_del}"):
                            aluno_del = AlunoModelo(None, cpf_int, None, None, None)
                            if self.controlador.deletar_aluno(aluno_del):
                                st.session_state.sucesso_aluno = "delecao"
                                st.session_state.cpf_deletado = cpf_int
                                st.session_state.nome_deletado = aluno[0]
                                st.rerun()
                            else:
                                st.error("Erro ao remover.")
                else:
                    st.error("Aluno não encontrado.")
            except Exception as e:
                st.error(f"Erro: {e}")

def main():
    st.title("Gestão de Alunos")
    
    nome_banco = "controle_academico.db"
    pagina = ControleAlunosPage(nome_banco)
    
    pagina.exibir_feedback()
    
    operacao = st.selectbox("Operação:", 
                           ["Listar Alunos", "Cadastrar Aluno", "Atualizar Aluno", "Deletar Aluno"])
    
    operations = {
        "Listar Alunos": pagina.listar_alunos,
        "Cadastrar Aluno": pagina.cadastrar_aluno,
        "Atualizar Aluno": pagina.atualizar_aluno,
        "Deletar Aluno": pagina.deletar_aluno
    }
    operations[operacao]()

if __name__ == "__main__":
    main()