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