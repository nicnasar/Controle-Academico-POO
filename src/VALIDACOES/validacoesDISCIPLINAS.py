import sqlite3
from MODELOS.disciplinasMODELO import DisciplinaModelo


class Validar:
    
    
    def __init__(self, caminho_banco):
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo toda vez
        self.caminho_banco = caminho_banco
        
        
    def disciplina_existe(self, codigo_disciplina):
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        # ir para a coluna "código"
        cursor.execute("SELECT codigo FROM Disciplina")
        
        # criar uma lista com todos os códigos
        codigos = cursor.fetchall()
        
        # comparar cada código com o recebido
        for codigo in codigos:
            if codigo_disciplina == codigo[0]:
                conexao.close()
                print(f"A disciplina de código {codigo} já existe!")
                return True
        conexao.close()
        return False        
        
        
    def valores_vazios(self, disciplina: DisciplinaModelo):
        
        # print("Checando valores vazios")
        
        # primeiro é melhor estabelecer uma conexão com o banco
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        
        # se o nome estiver vazio
        if disciplina.nome is None: # comparações com None, o correto é usar is ou is not
            cursor.execute("SELECT nome FROM Disciplina WHERE codigo = ?", (disciplina.codigo,))
            # ESSA DESGRAÇA DE FUNÇÃO SELECT RECEBE UMA TUPLAAAAAAAA
            nome_atual = cursor.fetchone()
            
            # como é uma tupla, o valor a ser usado é o primeiro
            disciplina.nome = nome_atual[0]
            
            
        if disciplina.carga_horaria is None:
            cursor.execute("SELECT carga_horaria FROM Disciplina WHERE codigo = ? ", (disciplina.codigo,))
            carga_horaria_atual = cursor.fetchone()
            disciplina.carga_horaria = carga_horaria_atual[0]
            
            
        if disciplina.nome_professor is None:
            cursor.execute("SELECT nome_professor FROM Disciplina WHERE codigo = ?", (disciplina.codigo,))
            nome_professor_atual = cursor.fetchone()
            disciplina.nome_professor = nome_professor_atual[0]
            
        conexao.commit() 
        conexao.close()
        # print("Valores vazios checados.")
        
        return disciplina
        
        