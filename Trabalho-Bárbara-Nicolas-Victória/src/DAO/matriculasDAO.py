# Barbára Lima
# Nicolas Nasário
# Victória Kallas

import sqlite3

from MODELOS.matriculasMODELO import MatriculaModelo
from VALIDACOES.validacoesMATRICULA import ValidarMatricula
from VALIDACOES.validacoesDISCIPLINAS import ValidarDisciplina
from VALIDACOES.validacoesALUNO import ValidarAluno
from VALIDACOES.validacoesMATRICULA import ValidarMatricula

class MatriculaDao:
    
    
    def __init__(self, caminho_banco):
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo toda vez
        self.caminho_banco = caminho_banco
        self.validar_disciplina = ValidarDisciplina(caminho_banco)
        self.validar_aluno = ValidarAluno(caminho_banco)
        self.validar_matricula = ValidarMatricula(caminho_banco)
        
    
    def matricular_aluno_dao(self, matricula: MatriculaModelo):
        
        # se a disciplina não existe, retornar falso, pedir para cadastrar
        if not self.validar_disciplina.disciplina_existe(matricula.codigo_disciplina):
            return False
        
        # se o cpf do aluno não está no banco, sair
        if not self.validar_aluno.cpf_igual(matricula.cpf_aluno):
            return False
        
        # checar se já está matriculado
        # se já está matriculado, retornar falso (sair)
        if self.validar_matricula.ja_cadastrado(matricula.codigo_disciplina, matricula.cpf_aluno):
            return False
        # na interface: "while(not matricular) ... if "sair": break"
        
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        cursor.execute(
            """INSERT INTO
                Matricula(
                    codigo_disciplina,
                    cpf_aluno,
                    data_matricula,
                    horario_matricula
                    )
                VALUES (?, ?, ?, ?)
            """,
            (
                matricula.codigo_disciplina,
                matricula.cpf_aluno,
                matricula.data_matricula,
                matricula.horario_matricula
            )
        )
        
        conexao.commit()
        conexao.close()
        
        return True
    
    
    def cancelar_matricula_dao(self, matricula: MatriculaModelo):
        
        # se a disciplina não existe, retornar falso, pedir para cadastrar
        if not self.validar_disciplina.disciplina_existe(matricula.codigo_disciplina):
            return False
        
        # se o cpf do aluno não está no banco, sair
        if not self.validar_aluno.cpf_igual(matricula.cpf_aluno):
            return False
    
        # checar se já está matriculado
        # se já está matriculado, retornar falso (sair)
        if not self.validar_matricula.ja_cadastrado(matricula.codigo_disciplina, matricula.cpf_aluno):
            return False
        # na interface: "while(not matricular) ... if "sair": break"
        
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        cursor.execute("DELETE FROM Matricula WHERE codigo_disciplina = ? AND cpf_aluno = ?", (matricula.codigo_disciplina, matricula.cpf_aluno))
        
        conexao.commit()
        conexao.close()
        return True
        
        
    def listar_matriculas_dao(self):
        
        with open(file="lista_matriculas.csv", mode="w") as lista_mat:
            
            # conecta no banco de dados
            conexao = sqlite3.connect(self.caminho_banco)
            cursor = conexao.cursor()

            # pega os dados
            cursor.execute(
                """
                SELECT 
                    codigo_disciplina, 
                    cpf_aluno, 
                    data_matricula, 
                    horario_matricula
                FROM Matricula
                """
            )
            
            # cria uma lista contendo os itens do banco de dados
            dados = cursor.fetchall()
            
            # cria o cabeçalho
            lista_mat.write("codigo_disciplina; cpf_aluno; data_matricula; horario_matricula\n")
            
            # insere os dados na planilha
            for linha in dados:
                lista_mat.write(f"{linha[0]};{linha[1]};{linha[2]};{linha[3]}\n")
            
            conexao.commit()
            conexao.close()
            
        return True


    def listar_matriculas_simples_dao(self):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT m.codigo_disciplina, d.nome as nome_disciplina, 
                   m.cpf_aluno, a.nome as nome_aluno,
                   m.data_matricula, m.horario_matricula 
            FROM Matricula m
            LEFT JOIN Disciplina d ON m.codigo_disciplina = d.codigo
            LEFT JOIN Aluno a ON m.cpf_aluno = a.cpf
        """)
        matriculas = cursor.fetchall()
        
        conexao.close()
        return matriculas
    
    def verificar_matricula_existente_dao(self, codigo_disciplina, cpf_aluno):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM Matricula WHERE codigo_disciplina = ? AND cpf_aluno = ?", 
                      (codigo_disciplina, cpf_aluno))
        existe = cursor.fetchone()
        
        conexao.close()
        return existe is not None    