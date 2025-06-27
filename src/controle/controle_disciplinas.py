import streamlit as st
from database.banco_de_dados import BancoDeDados
import csv
from io import StringIO


class Disciplina:
    def __init__(self, codigo, nome, carga_horaria, nome_professor):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.nome_professor = nome_professor


class ControleDisciplina:
    def __init__(self):
        self.db = BancoDeDados()

    def adicionar_disciplina(self, disciplina: Disciplina):
        if self.db.buscar_disciplina_por_codigo(disciplina.codigo):
            st.warning(f"Disciplina com código '{disciplina.codigo}' já existe.")
            return
        self.db.cadastrar_disciplina(
            disciplina.codigo,
            disciplina.nome,
            disciplina.carga_horaria,
            disciplina.nome_professor,
        )
        st.success(f"Disciplina '{disciplina.nome}' cadastrada com sucesso!")

    def atualizar_disciplina(
        self, codigo, nome=None, carga_horaria=None, nome_professor=None
    ):
        self.db.atualizar_disciplina(codigo, nome, carga_horaria, nome_professor)

    def buscar_disciplina(self, codigo):
        return self.db.buscar_disciplina_por_codigo(codigo)

    def listar_disciplinas(self):
        return self.db.listar_disciplinas()

    def remover_disciplina(self, codigo):
        if not self.db.buscar_disciplina_por_codigo(codigo):
            st.warning(f"Disciplina com código '{codigo}' não existe.")
            return
        self.db.remover_disciplina(codigo)
        st.success(f"Disciplina com código '{codigo}' removida com sucesso!")

    def exportar_csv(self):
        disciplinas = self.listar_disciplinas()
        output = StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["id", "codigo", "nome", "carga_horaria", "professor"])
        for d in disciplinas:
            writer.writerow(
                [d["id"], d["codigo"], d["nome"], d["carga_horaria"], d["professor"]]
            )
        return output.getvalue()


def pagina_controle_disciplinas():
    st.title("Controle de Disciplinas")
    controle = ControleDisciplina()
    aba = st.tabs(["Cadastrar", "Atualizar", "Remover", "Listar"])

    with aba[0]:
        st.header("Cadastrar Nova Disciplina")
        if "cadastrar_disciplina_success" not in st.session_state:
            st.session_state.cadastrar_disciplina_success = False
        with st.form("form_cadastrar", clear_on_submit=True):
            codigo = st.text_input("Código")
            nome = st.text_input("Nome")
            carga_horaria = st.text_input("Carga Horária")
            nome_professor = st.text_input("Nome do Professor")
            submitted = st.form_submit_button("Cadastrar")
            if submitted:
                if not (codigo and nome and carga_horaria and nome_professor):
                    st.warning("Preencha todos os campos!")
                else:
                    disciplina = Disciplina(
                        codigo, nome, carga_horaria, nome_professor
                    )
                    controle.adicionar_disciplina(disciplina)
                    st.session_state.cadastrar_disciplina_success = True
                    st.rerun()
        if st.session_state.cadastrar_disciplina_success:
            st.success("Disciplina cadastrada e campos limpos para novo cadastro!")
            st.session_state.cadastrar_disciplina_success = False

    with aba[1]:
        st.header("Atualizar Disciplina")
        with st.form("form_atualizar"):
            codigo = st.text_input("Código da Disciplina para Atualizar")
            buscar = st.form_submit_button("Buscar")
            if buscar and codigo:
                dados = controle.buscar_disciplina(codigo)
                if not dados:
                    st.warning("Disciplina não encontrada.")
                else:
                    nome = st.text_input("Nome", value=dados["nome"])
                    carga_horaria = st.text_input(
                        "Carga Horária", value=str(dados["carga_horaria"])
                    )
                    nome_professor = st.text_input(
                        "Nome do Professor", value=dados["professor"]
                    )
                    atualizar = st.form_submit_button("Atualizar")
                    if atualizar:
                        # Se o campo for deixado em branco, mantém o valor atual
                        nome_final = nome.strip() if nome and nome.strip() else dados['nome']
                        carga_final = carga_horaria.strip() if carga_horaria and carga_horaria.strip() else dados['carga_horaria']
                        prof_final = nome_professor.strip() if nome_professor and nome_professor.strip() else dados['professor']
                        controle.atualizar_disciplina(codigo, nome_final, carga_final, prof_final)

    with aba[2]:
        st.header("Remover Disciplina")
        with st.form("form_remover"):
            codigo = st.text_input("Código da Disciplina para Remover")
            remover = st.form_submit_button("Remover")
            if remover and codigo:
                controle.remover_disciplina(codigo)

    with aba[3]:
        st.header("Listar Disciplinas")
        disciplinas = controle.listar_disciplinas()
        if disciplinas:
            st.dataframe(disciplinas)
            csv_data = controle.exportar_csv()
            st.download_button(
                label="Exportar para CSV",
                data=csv_data,
                file_name="disciplinas.csv",
                mime="text/csv",
            )
        else:
            st.info("Nenhuma disciplina cadastrada.")

