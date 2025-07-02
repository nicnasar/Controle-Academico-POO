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
    
    
    def valores_vazios(self, aluno: AlunoModelo):
        
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        if aluno.nome is None:
            cursor.execute("SELECT nome FROM Aluno WHERE cpf = ?", (aluno.cpf,))
            nome_atual = cursor.fetchone()
            aluno.nome = nome_atual[0]
            
        if aluno.idade is None:
            cursor.execute("SELECT idade FROM Aluno WHERE cpf = ?", (aluno.cpf,))
            idade_atual = cursor.fetchone()
            aluno.idade = idade_atual[0]
            
        if aluno.email is None:
            cursor.execute("SELECT email FROM Aluno WHERE cpf = ?", (aluno.cpf,))
            email_atual = cursor.fetchone()
            aluno.email = email_atual[0]
            
            
        if aluno.endereco is None:
            cursor.execute("SELECT endereco FROM Aluno WHERE cpf = ?", (aluno.cpf,))
            endereco_atual = cursor.fetchone()
            aluno.endereco = endereco_atual[0]
            
        conexao.commit()
        conexao.close()
        
        return aluno
            
        