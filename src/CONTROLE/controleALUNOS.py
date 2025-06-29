from MODELOS.alunoMODELO import AlunoModelo
# da pasta MODELOS, importar do arquivo alunoMODELO a classe AlunoModelo
from DAO.alunoDAO import AlunoDao


class ControleAluno:
    
    def __init__(self, aluno: AlunoDao):
        self.aluno = aluno
        
    def cadastrar_aluno(self, aluno: AlunoModelo):
        try:
            self.aluno.inserir_aluno(aluno)
            return True
            
        except:
            raise Exception("Erro ao cadastrar aluno.")

    def listar_alunos(self):
        try:
            return self.aluno.listar_alunos()
        except:
            raise Exception("Erro ao listar alunos.")