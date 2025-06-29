import sqlite3

class Validar:
    
    
    def __init__(self, caminho_banco):
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo toda vez
        self.caminho_banco = caminho_banco
        
        
    def check_disciplina(self, codigo_disciplina):
            conexao = sqlite3.connect(self.caminho_banco)
            cursor = conexao.cursor()
            cursor.execute("SELECT codigo FROM Disciplina")
            codigos = cursor.fetchall()

            for codigo in codigos:
                if codigo_disciplina == codigo:
                    print("A disciplina possui o mesmo código de outra já cadastrada.")
                    return codigo