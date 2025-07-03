from MODELOS.alunoMODELO import AlunoModelo
# da pasta MODELOS, importar do arquivo alunoMODELO a classe AlunoModelo
from DAO.alunoDAO import AlunoDao


class ControleAluno:
    
    def __init__(self, aluno: AlunoDao):
        self.aluno = aluno
        
    def cadastrar_aluno(self, aluno: AlunoModelo):
        try:
            self.aluno.inserir_aluno_dao(aluno)
            return True
            
        except:
            raise Exception("Erro ao cadastrar aluno.")
        
        
    def atualizar_aluno(self, aluno: AlunoModelo):
        if self.aluno.atualizar_aluno_dao(aluno):
            print("Aluno(a) atualizado(a) com sucesso.")
            return True
        
        else:
            print("Erro ao atualizar aluno(a).")
            return False


    def deletar_aluno(self, aluno: AlunoModelo):
        if self.aluno.deletar_aluno_dao(aluno):
            print("Aluno removido com sucesso!")
            return True
        
        else:
            print("Aluno não encontrado no banco de dados!")
            return False
    
    
    def listar_alunos(self):
        pass