from MODELOS.matriculasMODELO import MatriculaModelo
from DAO.matriculasDAO import MatriculaDao


class ControleMatricula:
    
    
    def __init__(self, matricula_dao: MatriculaDao):
        self.matricula_dao = matricula_dao
        
        
    def matricular_aluno(self, matricula: MatriculaModelo):
        
        if self.matricula_dao.matricular_aluno_dao(matricula):
            print("Matrícula realizada!")
            return True
            
        else:
            print("Erro ao matricular aluno.")
            return False
        
    
    def cancelar_matricula(self, matricula: MatriculaModelo):
        
        if self.matricula_dao.cancelar_matricula_dao(matricula):
            print("Matrícula cancelada.")
            return True
        
        else:
            print("Erro ao cancelar matrícula.")
            return False
        
        
    def listar_dados_csv(self):
        
        if self.matricula_dao.listar_matriculas_dao():
            print("Matriculas exportadas!")
            return True
    
        else:
            print("Erro ao exportar matrículas.")
            return False
        
    
    def listar_todas_matriculas(self):
        try:
            return self.matricula_dao.listar_matriculas_simples_dao()
        except Exception as e:
            print(f"Erro ao listar matrículas: {e}")
            return []
    
    
    def verificar_matricula_existe(self, codigo_disciplina, cpf_aluno):
        try:
            return self.matricula_dao.verificar_matricula_existente_dao(codigo_disciplina, cpf_aluno)
        except Exception as e:
            print(f"Erro ao verificar matrícula: {e}")
            return False