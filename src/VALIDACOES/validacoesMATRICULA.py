import sqlite3
from MODELOS.disciplinasMODELO import DisciplinaModelo


class ValidarMatricula:
    
    def __init__(self, caminho_banco):
        self.caminho_banco = caminho_banco
        
    
    def ja_cadastrado(self, codigo_disciplina, cpf_aluno):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        # só pra ocupar espaço (e ficar [mais] legível)
        cursor.execute(
            """
            SELECT 
                codigo_disciplina, 
                cpf_aluno 
            FROM Matriculas
            """
        )
        
        # tinha como abstrair mais isso, mas eu preferi não.
        codigos_e_cpfs = cursor.fetchall() # tupla
        
        for (codigo, cpf) in codigos_e_cpfs:
            
            if (codigo_disciplina, cpf_aluno) == (codigo, cpf):
                conexao.close()
                print("O aluno já está cadastrado nesta diciplina!")
                return True
            
        conexao.close()
        return False