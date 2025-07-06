# não permitir que nada seja cadastrado caso algum item esteja em branco

# formatar dados de entrada. Ex.: <int> 1326402714 --> <str> "132.634.027-14", datas e hora também

# APENAS fazer isso no DISPLAY. No banco os dados devem estar crus

# criar funções para dar display nos dados de forma correta

# caso der erro ao cadastrar qualquer coisa, os dados devem permanecer na tela. Do contrário, eles devem ser apagados dos espaços

"""
Sistema de Controle Acadêmico

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
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MODELOS.alunoMODELO import AlunoModelo
from DAO.alunoDAO import AlunoDao
from CONTROLE.controleALUNOS import ControleAluno
from VALIDACOES.validacoesALUNO import ValidarAluno

from MODELOS.disciplinasMODELO import DisciplinaModelo
from DAO.disciplinasDAO import DisciplinaDao
from CONTROLE.controleDISCIPLINAS import ControleDisciplina

from MODELOS.matriculasMODELO import MatriculaModelo
from DAO.matriculasDAO import MatriculaDao
from CONTROLE.controleMATRICULAS import ControleMatricula

st.set_page_config(
    page_title="Sistema Acadêmico Completo",
    layout="wide"
)

NOME_BANCO = "controle_academico.db"

def get_controlador_aluno():
    return ControleAluno(AlunoDao(NOME_BANCO))

def get_controlador_disciplina():
    return ControleDisciplina(DisciplinaDao(NOME_BANCO))

def get_controlador_matricula():
    return ControleMatricula(MatriculaDao(NOME_BANCO))

def get_validador():
    return ValidarAluno(NOME_BANCO)

def formatar_cpf(cpf):
    cpf_str = str(cpf).zfill(11)
    return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"

def crud_alunos():
    st.header("Gestão de Alunos")
    
    if 'sucesso_aluno' not in st.session_state:
        st.session_state.sucesso_aluno = None
    if 'cpf_atualizado' not in st.session_state:
        st.session_state.cpf_atualizado = None
    if 'cpf_deletado' not in st.session_state:
        st.session_state.cpf_deletado = None
    if 'nome_deletado' not in st.session_state:
        st.session_state.nome_deletado = None
    
    if st.session_state.sucesso_aluno:
        if st.session_state.sucesso_aluno == "cadastro":
            st.success("Aluno cadastrado com sucesso!")
        elif st.session_state.sucesso_aluno == "atualizacao":
            st.success(f"Aluno CPF {formatar_cpf(st.session_state.cpf_atualizado)} atualizado com sucesso!")
        elif st.session_state.sucesso_aluno == "delecao":
            st.success(f"Aluno {st.session_state.nome_deletado} (CPF: {formatar_cpf(st.session_state.cpf_deletado)}) removido com sucesso!")
        
        st.session_state.sucesso_aluno = None
        st.session_state.cpf_atualizado = None
        st.session_state.cpf_deletado = None
        st.session_state.nome_deletado = None
    
    operacao = st.selectbox(
        "Escolha a operação:",
        ["Listar Alunos", "Cadastrar Aluno", "Atualizar Aluno", "Deletar Aluno"]
    )
    
    controlador = get_controlador_aluno()
    validador = get_validador()
    
    if operacao == "Listar Alunos":
        st.subheader("Lista de Alunos Cadastrados")
        
        alunos = controlador.listar_todos_alunos()
        
        if alunos:
            import pandas as pd
            df = pd.DataFrame(alunos, columns=["Nome", "CPF", "Idade", "Email", "Endereço"])
            df["CPF"] = df["CPF"].apply(formatar_cpf)
            
            st.dataframe(df, use_container_width=True)
            st.info(f"Total de alunos cadastrados: {len(alunos)}")
        else:
            st.warning("Nenhum aluno cadastrado no sistema.")
    
    elif operacao == "Cadastrar Aluno":
        st.subheader("Cadastrar Novo Aluno")
        
        if 'endereco_automatico' not in st.session_state:
            st.session_state.endereco_automatico = ""
        if 'cep_atual' not in st.session_state:
            st.session_state.cep_atual = ""
        if 'dados_form' not in st.session_state:
            st.session_state.dados_form = {
                'nome': '', 'cpf': '', 'idade': 18, 'email': '', 'cep': ''
            }
        
        with st.form("form_cadastrar_aluno", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input(
                    "Nome completo *", 
                    placeholder="Ex: João Silva",
                    value=st.session_state.dados_form.get('nome', '')
                )
                cpf = st.text_input(
                    "CPF (apenas números) *", 
                    placeholder="Ex: 12345678901", 
                    max_chars=11,
                    value=st.session_state.dados_form.get('cpf', '')
                )
                idade = st.number_input(
                    "Idade *", 
                    min_value=1, 
                    max_value=120, 
                    value=st.session_state.dados_form.get('idade', 18)
                )
            
            with col2:
                email = st.text_input(
                    "Email *", 
                    placeholder="Ex: joao@email.com",
                    value=st.session_state.dados_form.get('email', '')
                )
                
                cep = st.text_input(
                    "CEP", 
                    placeholder="Ex: 12345678", 
                    max_chars=8,
                    value=st.session_state.dados_form.get('cep', ''),
                    help="Digite 8 números para buscar automaticamente"
                )
                
                if cep != st.session_state.cep_atual:
                    st.session_state.cep_atual = cep
                    
                    if cep and len(cep) == 8 and cep.isdigit():
                        try:
                            validador = get_validador()
                            endereco_cep = validador.validar_CEP(cep)
                            if endereco_cep:
                                st.session_state.endereco_automatico = endereco_cep
                                st.session_state.dados_form = {
                                    'nome': nome, 'cpf': cpf, 'idade': idade, 
                                    'email': email, 'cep': cep
                                }
                                st.success("CEP encontrado! Endereço preenchido automaticamente.")
                                st.rerun()
                            else:
                                st.session_state.endereco_automatico = ""
                                st.warning("CEP não encontrado ou inválido.")
                        except Exception as e:
                            st.session_state.endereco_automatico = ""
                            st.error(f"Erro ao buscar CEP: {e}")
                    elif len(cep) < 8 and len(cep) > 0:
                        st.info(f"Digite mais {8-len(cep)} dígito(s)")
                        st.session_state.endereco_automatico = ""
                    elif not cep:
                        st.session_state.endereco_automatico = ""
                
                endereco = st.text_area(
                    "Endereço *", 
                    value=st.session_state.endereco_automatico,
                    placeholder="Ex: Rua das Flores, 123, Centro",
                    help="Será preenchido automaticamente se você digitar um CEP válido"
                )
                
                if st.session_state.endereco_automatico and cep and len(cep) == 8:
                    st.caption(f"Endereço encontrado pelo CEP: {cep}")
            
            submitted = st.form_submit_button("Cadastrar Aluno", type="primary")
            
            if submitted:
                st.session_state.dados_form = {
                    'nome': nome, 'cpf': cpf, 'idade': idade, 
                    'email': email, 'cep': cep
                }
                
                if not nome or not cpf or not email or not endereco:
                    st.error("Por favor, preencha todos os campos obrigatórios (*).")
                elif len(cpf) != 11 or not cpf.isdigit():
                    st.error("CPF deve conter exatamente 11 dígitos numéricos.")
                elif "@" not in email:
                    st.error("Email deve ter um formato válido.")
                else:
                    try:
                        cpf_int = int(cpf)
                        
                        if validador.cpf_igual(cpf_int):
                            st.error("Este CPF já está cadastrado no sistema!")
                        else:
                            aluno = AlunoModelo(nome, cpf_int, idade, email, endereco)
                            
                            if controlador.cadastrar_aluno(aluno):
                                st.session_state.sucesso_aluno = "cadastro"
                                st.session_state.endereco_automatico = ""
                                st.session_state.cep_atual = ""
                                st.session_state.dados_form = {
                                    'nome': '', 'cpf': '', 'idade': 18, 'email': '', 'cep': ''
                                }
                                st.rerun()
                            else:
                                st.error("Erro ao cadastrar aluno.")
                    
                    except ValueError:
                        st.error("CPF deve conter apenas números.")
                    except Exception as e:
                        st.error(f"Erro inesperado: {e}")
    
    elif operacao == "Atualizar Aluno":
        st.subheader("Atualizar Dados do Aluno")
        
        cpf_busca = st.text_input("Digite o CPF do aluno (apenas números):", max_chars=11)
        
        if cpf_busca and len(cpf_busca) == 11 and cpf_busca.isdigit():
            try:
                cpf_int = int(cpf_busca)
                aluno_atual = controlador.buscar_aluno_por_cpf(cpf_int)
                
                if aluno_atual:
                    st.success(f"Aluno encontrado: {aluno_atual[0]}")
                    
                    form_key = f"form_atualizar_aluno_{cpf_busca}_{hash(str(aluno_atual))}"
                    with st.form(form_key):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            novo_nome = st.text_input("Nome", value=aluno_atual[0])
                            nova_idade = st.number_input("Idade", min_value=1, max_value=120, value=aluno_atual[2])
                        
                        with col2:
                            novo_email = st.text_input("Email", value=aluno_atual[3])
                            novo_endereco = st.text_area("Endereço", value=aluno_atual[4])
                        
                        submitted = st.form_submit_button("Atualizar Dados", type="primary")
                        
                        if submitted:
                            if novo_nome and novo_email and novo_endereco:
                                try:
                                    aluno_atualizado = AlunoModelo(novo_nome, cpf_int, nova_idade, novo_email, novo_endereco)
                                    
                                    if controlador.atualizar_aluno(aluno_atualizado):
                                        st.session_state.sucesso_aluno = "atualizacao"
                                        st.session_state.cpf_atualizado = cpf_int
                                        st.rerun()
                                    else:
                                        st.error("Erro ao atualizar dados.")
                                
                                except Exception as e:
                                    st.error(f"Erro: {e}")
                            else:
                                st.error("Todos os campos são obrigatórios.")
                
                else:
                    st.error("Aluno não encontrado com este CPF.")
            
            except ValueError:
                st.error("CPF deve conter apenas números.")
    
    elif operacao == "Deletar Aluno":
        st.subheader("Remover Aluno do Sistema")
        
        st.warning("Esta ação é irreversível!")
        
        cpf_deletar = st.text_input("Digite o CPF do aluno a ser removido:", 
                                   max_chars=11, key="deletar_aluno_cpf")
        
        if cpf_deletar and len(cpf_deletar) == 11 and cpf_deletar.isdigit():
            try:
                cpf_int = int(cpf_deletar)
                aluno_encontrado = controlador.buscar_aluno_por_cpf(cpf_int)
                
                if aluno_encontrado:
                    st.info(f"**Aluno encontrado:**\n\n"
                           f"**Nome:** {aluno_encontrado[0]}\n\n"
                           f"**CPF:** {formatar_cpf(aluno_encontrado[1])}\n\n"
                           f"**Idade:** {aluno_encontrado[2]} anos\n\n"
                           f"**Email:** {aluno_encontrado[3]}\n\n"
                           f"**Endereço:** {aluno_encontrado[4]}")
                    
                    confirmar = st.checkbox("Confirmo que desejo remover este aluno permanentemente", 
                                           key=f"confirmar_delete_aluno_{cpf_deletar}")
                    
                    if confirmar:
                        if st.button("Confirmar Remoção", type="secondary", key=f"btn_delete_aluno_{cpf_deletar}"):
                            try:
                                aluno_deletar = AlunoModelo(None, cpf_int, None, None, None)
                                
                                if controlador.deletar_aluno(aluno_deletar):
                                    st.session_state.sucesso_aluno = "delecao"
                                    st.session_state.cpf_deletado = cpf_int
                                    st.session_state.nome_deletado = aluno_encontrado[0]
                                    st.rerun()
                                else:
                                    st.error("Erro ao remover aluno.")
                            
                            except Exception as e:
                                st.error(f"Erro: {e}")
                
                else:
                    st.error("Aluno não encontrado com este CPF.")
            
            except ValueError:
                st.error("CPF deve conter apenas números.")

def crud_disciplinas():
    st.header("Gestão de Disciplinas")
    
    if 'sucesso_disciplina' not in st.session_state:
        st.session_state.sucesso_disciplina = None
    if 'codigo_atualizado' not in st.session_state:
        st.session_state.codigo_atualizado = None
    if 'codigo_deletado' not in st.session_state:
        st.session_state.codigo_deletado = None
    
    if st.session_state.sucesso_disciplina:
        if st.session_state.sucesso_disciplina == "cadastro":
            st.success("Disciplina cadastrada com sucesso!")
        elif st.session_state.sucesso_disciplina == "atualizacao":
            st.success(f"Disciplina código {st.session_state.codigo_atualizado} atualizada com sucesso!")
        elif st.session_state.sucesso_disciplina == "delecao":
            st.success(f"Disciplina código {st.session_state.codigo_deletado} removida com sucesso!")
        
        st.session_state.sucesso_disciplina = None
        st.session_state.codigo_atualizado = None
        st.session_state.codigo_deletado = None
    
    operacao = st.selectbox(
        "Escolha a operação:",
        ["Listar Disciplinas", "Cadastrar Disciplina", "Atualizar Disciplina", "Deletar Disciplina"]
    )
    
    controlador = get_controlador_disciplina()
    
    if operacao == "Listar Disciplinas":
        st.subheader("Lista de Disciplinas Cadastradas")
        
        disciplinas = controlador.listar_todas_disciplinas()
        
        if disciplinas:
            import pandas as pd
            df = pd.DataFrame(disciplinas, columns=["Código", "Nome", "Carga Horária", "Professor"])
            
            st.dataframe(df, use_container_width=True)
            st.info(f"Total de disciplinas cadastradas: {len(disciplinas)}")
        else:
            st.warning("Nenhuma disciplina cadastrada no sistema.")
    
    elif operacao == "Cadastrar Disciplina":
        st.subheader("Cadastrar Nova Disciplina")
        
        with st.form("form_cadastrar_disciplina"):
            col1, col2 = st.columns(2)
            
            with col1:
                codigo = st.number_input("Código da Disciplina *", min_value=1, step=1)
                nome = st.text_input("Nome da Disciplina", placeholder="Ex: Cálculo I")
            
            with col2:
                carga_horaria = st.number_input("Carga Horária", min_value=0, step=1, value=0)
                nome_professor = st.text_input("Nome do Professor", placeholder="Ex: Dr. Silva")
            
            submitted = st.form_submit_button("Cadastrar Disciplina", type="primary")
            
            if submitted:
                try:
                    disciplina_existente = controlador.buscar_disciplina_por_codigo(codigo)
                    
                    if disciplina_existente:
                        st.error("Este código de disciplina já está cadastrado!")
                    else:
                        disciplina = DisciplinaModelo(
                            codigo, 
                            nome if nome else None, 
                            carga_horaria if carga_horaria > 0 else None, 
                            nome_professor if nome_professor else None
                        )
                        
                        if controlador.cadastrar_disciplina(disciplina):
                            st.session_state.sucesso_disciplina = "cadastro"
                            st.rerun()
                        else:
                            st.error("Erro ao cadastrar disciplina.")
                
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")
    
    elif operacao == "Atualizar Disciplina":
        st.subheader("Atualizar Dados da Disciplina")
        
        codigo_busca = st.number_input("Digite o código da disciplina:", 
                                      min_value=0, step=1, value=0)
        
        if codigo_busca > 0:
            try:
                disciplina_atual = controlador.buscar_disciplina_por_codigo(codigo_busca)
                
                if disciplina_atual:
                    st.success(f"Disciplina encontrada: {disciplina_atual[1] or 'Sem nome'}")
                    
                    form_key = f"form_atualizar_disciplina_{codigo_busca}_{hash(str(disciplina_atual))}"
                    with st.form(form_key):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            novo_nome = st.text_input("Nome", value=disciplina_atual[1] or "")
                            nova_carga = st.number_input("Carga Horária", min_value=0, value=disciplina_atual[2] or 0)
                        
                        with col2:
                            novo_professor = st.text_input("Professor", value=disciplina_atual[3] or "")
                        
                        submitted = st.form_submit_button("Atualizar Dados", type="primary")
                        
                        if submitted:
                            try:
                                disciplina_atualizada = DisciplinaModelo(
                                    codigo_busca,
                                    novo_nome if novo_nome else None,
                                    nova_carga if nova_carga > 0 else None,
                                    novo_professor if novo_professor else None
                                )
                                
                                if controlador.atualizar_disciplina(disciplina_atualizada):
                                    st.session_state.sucesso_disciplina = "atualizacao"
                                    st.session_state.codigo_atualizado = codigo_busca
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar dados.")
                            
                            except Exception as e:
                                st.error(f"Erro: {e}")
                
                else:
                    st.error("Disciplina não encontrada com este código.")
            
            except Exception as e:
                st.error(f"Erro: {e}")
    
    elif operacao == "Deletar Disciplina":
        st.subheader("Remover Disciplina do Sistema")
        
        st.warning("Esta ação é irreversível!")
        
        codigo_deletar = st.number_input("Digite o código da disciplina a ser removida:", 
                                        min_value=0, step=1, value=0)
        
        if codigo_deletar > 0:
            try:
                disciplina_encontrada = controlador.buscar_disciplina_por_codigo(codigo_deletar)
                
                if disciplina_encontrada:
                    st.info(f"**Disciplina encontrada:**\n\n"
                           f"**Código:** {disciplina_encontrada[0]}\n\n"
                           f"**Nome:** {disciplina_encontrada[1] or 'Não informado'}\n\n"
                           f"**Carga Horária:** {disciplina_encontrada[2] or 'Não informada'}\n\n"
                           f"**Professor:** {disciplina_encontrada[3] or 'Não informado'}")
                    
                    confirmar_key = f"confirmar_delete_disciplina_{codigo_deletar}_{hash(str(disciplina_encontrada))}"
                    confirmar = st.checkbox("Confirmo que desejo remover esta disciplina permanentemente", 
                                           key=confirmar_key)
                    
                    if confirmar:
                        btn_key = f"btn_delete_disciplina_{codigo_deletar}_{hash(str(disciplina_encontrada))}"
                        if st.button("Confirmar Remoção", type="secondary", key=btn_key):
                            try:
                                disciplina_deletar = DisciplinaModelo(codigo_deletar, None, None, None)
                                
                                if controlador.deletar_disciplina(disciplina_deletar):
                                    st.session_state.sucesso_disciplina = "delecao"
                                    st.session_state.codigo_deletado = codigo_deletar
                                    st.rerun() 
                                else:
                                    st.error("Erro ao remover disciplina.")
                            
                            except Exception as e:
                                st.error(f"Erro: {e}")
                
                else:
                    st.error("Disciplina não encontrada com este código.")
            
            except Exception as e:
                st.error(f"Erro: {e}")

def crud_matriculas():
    st.header("Gestão de Matrículas")
    
    if 'sucesso_matricula' not in st.session_state:
        st.session_state.sucesso_matricula = None
    if 'aluno_matriculado' not in st.session_state:
        st.session_state.aluno_matriculado = None
    if 'disciplina_matriculada' not in st.session_state:
        st.session_state.disciplina_matriculada = None
    if 'cpf_cancelado' not in st.session_state:
        st.session_state.cpf_cancelado = None
    if 'nome_aluno_cancelado' not in st.session_state:
        st.session_state.nome_aluno_cancelado = None
    if 'codigo_disciplina_cancelada' not in st.session_state:
        st.session_state.codigo_disciplina_cancelada = None
    if 'nome_disciplina_cancelada' not in st.session_state:
        st.session_state.nome_disciplina_cancelada = None
    
    if st.session_state.sucesso_matricula:
        if st.session_state.sucesso_matricula == "realizacao":
            st.success(f"Matrícula realizada com sucesso!\n\n"
                      f"**Aluno:** {st.session_state.aluno_matriculado[0]} (CPF: {formatar_cpf(st.session_state.aluno_matriculado[1])})\n\n"
                      f"**Disciplina:** {st.session_state.disciplina_matriculada[0]} - {st.session_state.disciplina_matriculada[1] or 'Sem nome'}")
        elif st.session_state.sucesso_matricula == "cancelamento":
            st.success(f"Matrícula cancelada com sucesso!\n\n"
                      f"**Aluno:** {st.session_state.nome_aluno_cancelado} (CPF: {formatar_cpf(st.session_state.cpf_cancelado)})\n\n"
                      f"**Disciplina:** {st.session_state.codigo_disciplina_cancelada} - {st.session_state.nome_disciplina_cancelada or 'Sem nome'}")
        
        st.session_state.sucesso_matricula = None
        st.session_state.aluno_matriculado = None
        st.session_state.disciplina_matriculada = None
        st.session_state.cpf_cancelado = None
        st.session_state.nome_aluno_cancelado = None
        st.session_state.codigo_disciplina_cancelada = None
        st.session_state.nome_disciplina_cancelada = None
    
    if 'cancelando_matricula' not in st.session_state:
        st.session_state.cancelando_matricula = False
    
    operacao = st.selectbox(
        "Escolha a operação:",
        ["Listar Matrículas", "Realizar Matrícula", "Cancelar Matrícula"]
    )
    
    controlador = get_controlador_matricula()
    controlador_disciplina = get_controlador_disciplina()
    controlador_aluno = get_controlador_aluno()
    
    if operacao == "Listar Matrículas":
        st.subheader("Lista de Matrículas Realizadas")
        
        matriculas = controlador.listar_todas_matriculas()
        
        if matriculas:
            import pandas as pd
            df = pd.DataFrame(matriculas, columns=[
                "Código Disciplina", "Nome Disciplina", "CPF Aluno", 
                "Nome Aluno", "Data Matrícula", "Horário Matrícula"
            ])
            df["CPF Aluno"] = df["CPF Aluno"].apply(formatar_cpf)
            
            st.dataframe(df, use_container_width=True)
            st.info(f"Total de matrículas realizadas: {len(matriculas)}")
        else:
            st.warning("Nenhuma matrícula realizada no sistema.")
    
    elif operacao == "Realizar Matrícula":
        st.subheader("Realizar Nova Matrícula")
        
        disciplinas = controlador_disciplina.listar_todas_disciplinas()
        alunos = controlador_aluno.listar_todos_alunos()
        
        if not disciplinas:
            st.error("Não há disciplinas cadastradas. Cadastre disciplinas primeiro.")
            return
        
        if not alunos:
            st.error("Não há alunos cadastrados. Cadastre alunos primeiro.")
            return
        
        with st.form("form_matricular"):
            col1, col2 = st.columns(2)
            
            with col1:
                opcoes_disciplinas = [f"{d[0]} - {d[1] or 'Sem nome'}" for d in disciplinas]
                disciplina_selecionada = st.selectbox("Selecione a Disciplina *", opcoes_disciplinas)
                
                cpf_aluno_input = st.text_input("Digite o CPF do Aluno (apenas números) *", 
                                              placeholder="Ex: 12345678901", max_chars=11)
            
            with col2:
                data_matricula = datetime.now().date()
                horario_matricula = datetime.now().time()
                
                st.date_input("Data da Matrícula", value=data_matricula, disabled=True)
                st.time_input("Horário da Matrícula", value=horario_matricula, disabled=True)
                st.caption("Data e horário são definidos automaticamente como o momento atual")
            
            submitted = st.form_submit_button("Realizar Matrícula", type="primary")
            
            if submitted:
                if not cpf_aluno_input:
                    st.error("Por favor, digite o CPF do aluno.")
                elif len(cpf_aluno_input) != 11 or not cpf_aluno_input.isdigit():
                    st.error("CPF deve conter exatamente 11 dígitos numéricos.")
                else:
                    try:
                        codigo_disciplina = int(disciplina_selecionada.split(" - ")[0])
                        cpf_aluno = int(cpf_aluno_input)
                        
                        aluno_encontrado = controlador_aluno.buscar_aluno_por_cpf(cpf_aluno)
                        
                        if not aluno_encontrado:
                            st.error("Aluno não encontrado com este CPF. Verifique se o CPF está correto ou cadastre o aluno primeiro.")
                        elif controlador.verificar_matricula_existe(codigo_disciplina, cpf_aluno):
                            st.error("Este aluno já está matriculado nesta disciplina!")
                        else:
                            matricula = MatriculaModelo(
                                codigo_disciplina,
                                cpf_aluno,
                                data_matricula.strftime("%d/%m/%Y"),
                                horario_matricula.strftime("%H:%M")
                            )
                            
                            if controlador.matricular_aluno(matricula):
                                disciplina_dados = controlador_disciplina.buscar_disciplina_por_codigo(codigo_disciplina)
                                
                                st.session_state.sucesso_matricula = "realizacao"
                                st.session_state.aluno_matriculado = (aluno_encontrado[0], cpf_aluno)
                                st.session_state.disciplina_matriculada = (codigo_disciplina, disciplina_dados[1] if disciplina_dados else 'Sem nome')
                                st.rerun()
                            else:
                                st.error("Erro ao realizar matrícula.")
                    
                    except Exception as e:
                        st.error(f"Erro inesperado: {e}")
    
    elif operacao == "Cancelar Matrícula":
        st.subheader("Cancelar Matrícula")
        
        st.warning("Esta ação é irreversível!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            codigo_disciplina_input = st.number_input("Digite o código da disciplina:", min_value=0, step=1, value=0, key="cancelar_disciplina")
        
        with col2:
            cpf_aluno_input = st.text_input("Digite o CPF do aluno (apenas números):", 
                                          placeholder="Ex: 12345678901", max_chars=11, key="cancelar_cpf")
        
        if codigo_disciplina_input > 0 and cpf_aluno_input and len(cpf_aluno_input) == 11 and cpf_aluno_input.isdigit():
            try:
                cpf_aluno = int(cpf_aluno_input)
                
                aluno_encontrado = controlador_aluno.buscar_aluno_por_cpf(cpf_aluno)
                if not aluno_encontrado:
                    st.error("Aluno não encontrado com este CPF.")
                    return
                
                disciplina_encontrada = controlador_disciplina.buscar_disciplina_por_codigo(codigo_disciplina_input)
                if not disciplina_encontrada:
                    st.error("Disciplina não encontrada com este código.")
                    return
                
                if not controlador.verificar_matricula_existe(codigo_disciplina_input, cpf_aluno):
                    st.error("Matrícula não encontrada. Verifique se o aluno está realmente matriculado nesta disciplina.")
                    return
                
                matricula_dados = [codigo_disciplina_input, disciplina_encontrada[1], cpf_aluno, aluno_encontrado[0]]
                
                st.success("Matrícula encontrada!")
                st.info(f"**Matrícula a ser cancelada:**\n\n"
                       f"**Disciplina:** {matricula_dados[0]} - {matricula_dados[1] or 'Sem nome'}\n\n"
                       f"**Aluno:** {formatar_cpf(matricula_dados[2])} - {matricula_dados[3] or 'Sem nome'}")
                
                confirmar = st.checkbox("Confirmo que desejo cancelar esta matrícula permanentemente")
                
                if confirmar:
                    if st.button("Confirmar Cancelamento", type="secondary", disabled=st.session_state.get('cancelando_matricula', False)):
                        st.session_state.cancelando_matricula = True
                        
                        try:
                            matricula_cancelar = MatriculaModelo(
                                matricula_dados[0],
                                matricula_dados[2],
                                None,
                                None
                            )
                            
                            if controlador.cancelar_matricula(matricula_cancelar):
                                st.session_state.sucesso_matricula = "cancelamento"
                                st.session_state.cpf_cancelado = matricula_dados[2]
                                st.session_state.nome_aluno_cancelado = matricula_dados[3]
                                st.session_state.codigo_disciplina_cancelada = matricula_dados[0]
                                st.session_state.nome_disciplina_cancelada = matricula_dados[1]
                                
                                if 'cancelando_matricula' in st.session_state:
                                    del st.session_state.cancelando_matricula
                                
                                st.rerun()
                            else:
                                st.error("Erro ao cancelar matrícula.")
                                if 'cancelando_matricula' in st.session_state:
                                    del st.session_state.cancelando_matricula
                        
                        except Exception as e:
                            st.error(f"Erro: {e}")
                            if 'cancelando_matricula' in st.session_state:
                                del st.session_state.cancelando_matricula
            
            except ValueError:
                st.error("CPF deve conter apenas números.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
        
        elif cpf_aluno_input and len(cpf_aluno_input) != 11:
            st.warning("CPF deve conter exatamente 11 dígitos.")
        elif cpf_aluno_input and not cpf_aluno_input.isdigit():
            st.warning("CPF deve conter apenas números.")

def main():
    st.title("Sistema de Controle Acadêmico")
    
    st.sidebar.title("Menu Principal")
    modulo = st.sidebar.selectbox(
        "Escolha o módulo:",
        ["Início", "Controle de Alunos", "Controle de Disciplinas", "Controle de Matrículas"]
    )
    
    if modulo == "Início":
        st.header("Bem-vindo ao Sistema de Controle Acadêmico!")
        
        col1, col2, col3 = st.columns(3)
        
        controlador_aluno = get_controlador_aluno()
        controlador_disciplina = get_controlador_disciplina()
        controlador_matricula = get_controlador_matricula()
        
        with col1:
            alunos = controlador_aluno.listar_todos_alunos()
            st.metric("Total de Alunos", len(alunos))
        
        with col2:
            disciplinas = controlador_disciplina.listar_todas_disciplinas()
            st.metric("Total de Disciplinas", len(disciplinas))
        
        with col3:
            matriculas = controlador_matricula.listar_todas_matriculas()
            st.metric("Total de Matrículas", len(matriculas))
        
        st.markdown("""
        ### Funcionalidades do Sistema:
        
        - **Controle de Alunos**: Cadastro, atualização, listagem e exclusão de alunos
        - **Controle de Disciplinas**: Gestão completa das disciplinas oferecidas
        - **Controle de Matrículas**: Realização e cancelamento de matrículas
        
        ### Como usar:
        1. Use o menu lateral para navegar entre os módulos
        2. Cada módulo possui suas operações específicas de CRUD
        3. Siga as instruções em cada tela para realizar as operações
        
        **Nota**: Certifique-se de ter alunos e disciplinas cadastrados antes de realizar matrículas.
        """)
    
    elif modulo == "Controle de Alunos":
        crud_alunos()
    
    elif modulo == "Controle de Disciplinas":
        crud_disciplinas()
    
    elif modulo == "Controle de Matrículas":
        crud_matriculas()

if __name__ == "__main__":
    main()