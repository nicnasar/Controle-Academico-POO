from MODELOS.disciplinasMODELO import DisciplinaModelo
from DAO.disciplinasDAO import DisciplinaDao


# saídas devem estar no CONTROLE, nada de bagunçar mais o DAO

class ControleDisciplina:
    
    
    def __init__(self, disciplina: DisciplinaDao):
        self.disciplina = disciplina
        
    
    def cadastrar_disciplina(self, disciplina: DisciplinaModelo):
        try:
            # detalhe que self.disciplina != disciplina
            self.disciplina.cadastrar_disciplina(disciplina)
            print("Disciplina cadastrada com sucesso!")
            return True
        
        except:
            print("Erro ao cadastrar disciplina.")
            return False
        
        
    def atualizar_disciplina(self, disciplina: DisciplinaModelo):
        try:
            self.disciplina.atualizar_disciplina_dao(disciplina)
            print("Disciplina atualizada com sucesso!")
            return True
        
        except:
            print("Erro ao atualizar disciplina.")
            return False    