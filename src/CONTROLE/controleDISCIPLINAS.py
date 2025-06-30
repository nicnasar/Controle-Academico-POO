from MODELOS.disciplinasMODELO import DisciplinaModelo
from DAO.disciplinasDAO import DisciplinaDao


# saídas devem estar no CONTROLE, nada de bagunçar mais o DAO

class ControleDisciplina:
    
    
    def __init__(self, disciplina: DisciplinaDao):
        self.disciplina = disciplina
        
    
    def cadastrar_disciplina(self, disciplina: DisciplinaModelo):
        try:
            # detalhe que self.disciplina != disciplina
            self.disciplina.cadastrar_disciplina_dao(disciplina)
            print("Disciplina cadastrada com sucesso!")
            return True
        
        except:
            print("Erro ao cadastrar disciplina.")
            return False
        
        
    def atualizar_disciplina(self, disciplina: DisciplinaModelo):
        
        if self.disciplina.atualizar_disciplina_dao(disciplina):
            print("Disciplina atualizada com sucesso!")
            return True
        
        else:
            print("Erro ao atualizar disciplina.")
            return False 
        
        
    def deletar_disciplina(self, disciplina: DisciplinaModelo):
        
        if self.disciplina.remover_disciplina_dao(disciplina.codigo):
            print("Disciplina deletada com sucesso!")
            return True
        else:
            print("Erro ao deletar disciplina.")
            return False
        
    def listar_dados(self):
        
        if self.disciplina.listar_disciplinas_dao():
            print("Dados listados com sucesso!")
        
        else:
            print("Erro ao listar os dados.")