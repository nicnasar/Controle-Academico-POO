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
        
        
        