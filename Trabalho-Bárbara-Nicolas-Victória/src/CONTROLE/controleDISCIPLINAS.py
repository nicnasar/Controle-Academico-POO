# Barbára Lima
# Nicolas Nasário
# Victória Kallas

from MODELOS.disciplinasMODELO import DisciplinaModelo
from DAO.disciplinasDAO import DisciplinaDao


# saídas devem estar no CONTROLE, nada de bagunçar mais o DAO

class ControleDisciplina:
    
    #self.disciplina_dao é um atributo da classe ControleDisciplina que armazena uma instância da classe DisciplinaDao.
    
    def __init__(self, disciplina_dao: DisciplinaDao):
        self.disciplina_dao = disciplina_dao
        
        
    def cadastrar_disciplina(self, disciplina: DisciplinaModelo):
        try:
            # detalhe que self.disciplina_dao != disciplina
            self.disciplina_dao.cadastrar_disciplina_dao(disciplina)
            print("Disciplina cadastrada com sucesso!")
            return True
        
        except:
            print("Erro ao cadastrar disciplina.")
            return False
        
        
    def atualizar_disciplina(self, disciplina: DisciplinaModelo):
        
        if self.disciplina_dao.atualizar_disciplina_dao(disciplina):
            print("Disciplina atualizada com sucesso!")
            return True
        
        else:
            print("Erro ao atualizar disciplina.")
            return False 
        
        
    def deletar_disciplina(self, disciplina: DisciplinaModelo):
        
        if self.disciplina_dao.remover_disciplina_dao(disciplina.codigo):
            print("Disciplina deletada com sucesso!")
            return True
        else:
            print("Erro ao deletar disciplina.")
            return False
        
        
    def listar_dados(self):
        
        if self.disciplina_dao.listar_disciplinas_dao():
            print("Dados listados com sucesso!")
        
        else:
            print("Erro ao listar os dados.")

    
    def buscar_disciplina_por_codigo(self, codigo):
        try:
            return self.disciplina_dao.buscar_disciplina_por_codigo_dao(codigo)
        except Exception as e:
            print(f"Erro ao buscar disciplina: {e}")
            return None
    
   
    def listar_todas_disciplinas(self):
        try:
            return self.disciplina_dao.listar_disciplinas_simples_dao()
        except Exception as e:
            print(f"Erro ao listar disciplinas: {e}")
            return []