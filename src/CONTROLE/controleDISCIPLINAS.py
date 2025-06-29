from MODELOS.disciplinasMODELO import DisciplinaModelo
from DAO.disciplinasDAO import DisciplinaDao


class ControleDisciplina:
    
    
    def __init__(self, disciplina: DisciplinaDao):
        self.disciplina = disciplina
        
    
    def cadastrar_disciplina(self, disciplina: DisciplinaModelo):
        try:
            # detalhe que self.disciplina != disciplina
            self.disciplina.cadastrar_disciplina(disciplina)
            return True
        
        except:
            print("Erro ao cadastrar disciplina.")
            return False
            