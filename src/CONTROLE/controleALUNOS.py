from src.MODELOS.alunoMODELO import AlunoModelo
# da pasta MODELOS, importar do arquivo alunoMODELO a classe AlunoModelo
from src.DAO.alunoDAO import AlunoDao


class ControleAluno:
    
    def __init__(self, aluno: AlunoDao):
        self.aluno = aluno
        
    def cadastrar_aluno(self, aluno: AlunoModelo):
        try:
            AlunoDao().inserir_aluno(aluno)
            return True
            
        except:
            raise Exception("Erro ao cadastrar aluno.")
