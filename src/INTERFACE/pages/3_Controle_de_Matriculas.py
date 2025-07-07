# Barbára Lima

import streamlit as st
import pandas as pd
import sys
import os


from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from MODELOS.matriculasMODELO import MatriculaModelo
from DAO.matriculasDAO import MatriculaDao
from CONTROLE.controleMATRICULAS import ControleMatricula
from DAO.alunoDAO import AlunoDao
from CONTROLE.controleALUNOS import ControleAluno
from DAO.disciplinasDAO import DisciplinaDao
from CONTROLE.controleDISCIPLINAS import ControleDisciplina

st.set_page_config(
    page_title="Controle de Matrículas",
    layout="wide"
)

class ControleMatriculasPage:
    """Classe responsável pela interface de controle de matrículas"""
    
    def __init__(self, nome_banco):
        self.nome_banco = nome_banco
        self.controlador = ControleMatricula(MatriculaDao(nome_banco))
        self.controlador_aluno = ControleAluno(AlunoDao(nome_banco))
        self.controlador_disciplina = ControleDisciplina(DisciplinaDao(nome_banco))
        self._init_session()
    
    def _init_session(self):
        """Inicializa variáveis de sessão"""
        defaults = {
            'sucesso_matricula': None,
            'aluno_matriculado': None,
            'disciplina_matriculada': None,
            'cpf_cancelado': None,
            'nome_aluno_cancelado': None,
            'codigo_disciplina_cancelada': None,
            'nome_disciplina_cancelada': None,
            'cancelando_matricula': False
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
        if st.session_state.sucesso_matricula:
            if st.session_state.sucesso_matricula == "realizacao":
                st.success(f"Matrícula realizada com sucesso!\n\n"
                          f"**Aluno:** {st.session_state.aluno_matriculado[0]} (CPF: {self.formatar_cpf(st.session_state.aluno_matriculado[1])})\n\n"
                          f"**Disciplina:** {st.session_state.disciplina_matriculada[0]} - {st.session_state.disciplina_matriculada[1] or 'Sem nome'}")
            elif st.session_state.sucesso_matricula == "cancelamento":
                st.success(f"Matrícula cancelada com sucesso!\n\n"
                          f"**Aluno:** {st.session_state.nome_aluno_cancelado} (CPF: {self.formatar_cpf(st.session_state.cpf_cancelado)})\n\n"
                          f"**Disciplina:** {st.session_state.codigo_disciplina_cancelada} - {st.session_state.nome_disciplina_cancelada or 'Sem nome'}")
            
            for key in ['sucesso_matricula', 'aluno_matriculado', 'disciplina_matriculada', 
                       'cpf_cancelado', 'nome_aluno_cancelado', 'codigo_disciplina_cancelada', 'nome_disciplina_cancelada']:
                st.session_state[key] = None
    
    def listar_matriculas(self):
        """Lista todas as matrículas"""
        st.subheader("Lista de Matrículas Realizadas")
        matriculas = self.controlador.listar_todas_matriculas()
        
        if matriculas:
            df = pd.DataFrame(matriculas, columns=[
                "Código Disciplina", "Nome Disciplina", "CPF Aluno", 
                "Nome Aluno", "Data Matrícula", "Horário Matrícula"
            ])
            df["CPF Aluno"] = df["CPF Aluno"].apply(self.formatar_cpf)
            st.dataframe(df, use_container_width=True)
            st.info(f"Total: {len(matriculas)} matrículas")
        else:
            st.warning("Nenhuma matrícula realizada.")
    
    def realizar_matricula(self):
        """Formulário para realizar matrícula"""
        st.subheader("Realizar Nova Matrícula")
        
        disciplinas = self.controlador_disciplina.listar_todas_disciplinas()
        alunos = self.controlador_aluno.listar_todos_alunos()
        
        if not disciplinas:
            return st.error("Não há disciplinas cadastradas. Cadastre disciplinas primeiro.")
        if not alunos:
            return st.error("Não há alunos cadastrados. Cadastre alunos primeiro.")
        
        with st.form("form_matricular"):
            col1, col2 = st.columns(2)
            
            with col1:
                opcoes_disciplinas = [f"{d[0]} - {d[1] or 'Sem nome'}" for d in disciplinas]
                disciplina_selecionada = st.selectbox("Disciplina *", opcoes_disciplinas)
                cpf_aluno = st.text_input("CPF do Aluno *", placeholder="12345678901", max_chars=11)
            
            with col2:
                data_matricula = datetime.now().date()
                horario_matricula = datetime.now().time()
                st.date_input("Data", value=data_matricula, disabled=True)
                st.time_input("Horário", value=horario_matricula, disabled=True)
                st.caption("Data e horário automáticos")
            
            if st.form_submit_button("Realizar Matrícula", type="primary"):
                self._processar_matricula(disciplina_selecionada, cpf_aluno, data_matricula, horario_matricula)
    
    def _processar_matricula(self, disciplina_selecionada, cpf_aluno_input, data_matricula, horario_matricula):
        """Processa a matrícula"""
        if not cpf_aluno_input or len(cpf_aluno_input) != 11 or not cpf_aluno_input.isdigit():
            return st.error("CPF deve ter 11 dígitos numéricos.")
        
        try:
            codigo_disciplina = int(disciplina_selecionada.split(" - ")[0])
            cpf_aluno = int(cpf_aluno_input)
            
            aluno = self.controlador_aluno.buscar_aluno_por_cpf(cpf_aluno)
            if not aluno:
                return st.error("Aluno não encontrado.")
            
            if self.controlador.verificar_matricula_existe(codigo_disciplina, cpf_aluno):
                return st.error("Aluno já matriculado nesta disciplina!")
            
            matricula = MatriculaModelo(
                codigo_disciplina,
                cpf_aluno,
                data_matricula.strftime("%d/%m/%Y"),
                horario_matricula.strftime("%H:%M")
            )
            
            if self.controlador.matricular_aluno(matricula):
                disciplina_dados = self.controlador_disciplina.buscar_disciplina_por_codigo(codigo_disciplina)
                st.session_state.sucesso_matricula = "realizacao"
                st.session_state.aluno_matriculado = (aluno[0], cpf_aluno)
                st.session_state.disciplina_matriculada = (codigo_disciplina, disciplina_dados[1] if disciplina_dados else 'Sem nome')
                st.rerun()
            else:
                st.error("Erro ao realizar matrícula.")
        except Exception as e:
            st.error(f"Erro: {e}")
    
    def cancelar_matricula(self):
        """Formulário para cancelar matrícula"""
        st.subheader("Cancelar Matrícula")
        st.warning("Ação irreversível!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            codigo_disciplina = st.number_input("Código da disciplina:", min_value=0, step=1, value=0, key="cancelar_disciplina")
        
        with col2:
            cpf_aluno = st.text_input("CPF do aluno:", placeholder="12345678901", max_chars=11, key="cancelar_cpf")
        
        if codigo_disciplina > 0 and cpf_aluno and len(cpf_aluno) == 11 and cpf_aluno.isdigit():
            self._processar_cancelamento(codigo_disciplina, cpf_aluno)
        elif cpf_aluno and (len(cpf_aluno) != 11 or not cpf_aluno.isdigit()):
            st.warning("CPF deve ter 11 dígitos numéricos.")
    
    def _processar_cancelamento(self, codigo_disciplina, cpf_aluno_input):
        """Processa o cancelamento"""
        try:
            cpf_aluno = int(cpf_aluno_input)
            
            aluno = self.controlador_aluno.buscar_aluno_por_cpf(cpf_aluno)
            disciplina = self.controlador_disciplina.buscar_disciplina_por_codigo(codigo_disciplina)
            
            if not aluno:
                return st.error("Aluno não encontrado.")
            if not disciplina:
                return st.error("Disciplina não encontrada.")
            if not self.controlador.verificar_matricula_existe(codigo_disciplina, cpf_aluno):
                return st.error("Matrícula não encontrada.")
            
            st.success("Matrícula encontrada!")
            st.info(f"**Disciplina:** {codigo_disciplina} - {disciplina[1] or 'Sem nome'}\n\n"
                   f"**Aluno:** {self.formatar_cpf(cpf_aluno)} - {aluno[0]}")
            
            if st.checkbox("Confirmar cancelamento"):
                if st.button("Cancelar Matrícula", type="secondary", disabled=st.session_state.get('cancelando_matricula', False)):
                    self._executar_cancelamento(codigo_disciplina, cpf_aluno, aluno[0], disciplina[1])
        
        except Exception as e:
            st.error(f"Erro: {e}")
    
    def _executar_cancelamento(self, codigo_disciplina, cpf_aluno, nome_aluno, nome_disciplina):
        """Executa o cancelamento"""
        st.session_state.cancelando_matricula = True
        
        try:
            matricula = MatriculaModelo(codigo_disciplina, cpf_aluno, None, None)
            
            if self.controlador.cancelar_matricula(matricula):
                st.session_state.sucesso_matricula = "cancelamento"
                st.session_state.cpf_cancelado = cpf_aluno
                st.session_state.nome_aluno_cancelado = nome_aluno
                st.session_state.codigo_disciplina_cancelada = codigo_disciplina
                st.session_state.nome_disciplina_cancelada = nome_disciplina
                
                if 'cancelando_matricula' in st.session_state:
                    del st.session_state.cancelando_matricula
                st.rerun()
            else:
                st.error("Erro ao cancelar.")
                if 'cancelando_matricula' in st.session_state:
                    del st.session_state.cancelando_matricula
        except Exception as e:
            st.error(f"Erro: {e}")
            if 'cancelando_matricula' in st.session_state:
                del st.session_state.cancelando_matricula

def main():
    st.title("Gestão de Matrículas")
    
    nome_banco = "controle_academico.db"
    pagina = ControleMatriculasPage(nome_banco)
    
    pagina.exibir_feedback()
    
    operacao = st.selectbox("Operação:", 
                           ["Listar Matrículas", "Realizar Matrícula", "Cancelar Matrícula"])
    
    operations = {
        "Listar Matrículas": pagina.listar_matriculas,
        "Realizar Matrícula": pagina.realizar_matricula,
        "Cancelar Matrícula": pagina.cancelar_matricula
    }
    operations[operacao]()

if __name__ == "__main__":
    main()