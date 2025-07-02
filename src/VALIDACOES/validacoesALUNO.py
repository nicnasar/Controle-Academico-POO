import sqlite3
from MODELOS.alunoMODELO import AlunoModelo


class ValidarAluno:
    
    
    def __init__(self, caminho_banco):
        self.caminho_banco = caminho_banco
        
        
    def cpf_igual(self, CPF):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        cursor.execute("SELECT cpf FROM Aluno")
        
        cpfs = cursor.fetchall()
        
        for cpf in cpfs:
            if CPF == cpf[0]:
                conexao.close()
                print(f"O CPF cadastrado já existe!")
                return True
            
        conexao.close()
        return False
    
    