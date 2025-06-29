import sqlite3

#    PASTA   arqUIVO                  ClaSse
from MODELOS.disciplinasMODELO import DisciplinaModelo
from VALIDACOES.validacoesDISCIPLINAS import Validar


class DisciplinaDao:
    
    
    def __init__(self, caminho_banco):
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo toda vez
        self.caminho_banco = caminho_banco
        self.validar = Validar(caminho_banco)
            
            
    # não permitir o usuário cadastrar alguma disciplina sem todos os campos preenchidos
    def cadastrar_disciplina(self, disciplina: DisciplinaModelo):
        
        if self.validar.check_disciplina(disciplina.codigo):
            return False
        # colocar futuramente qual o nome da disciplina
        
        conexao = sqlite3.connect(self.caminho_banco) # abre
        cursor = conexao.cursor() # cria um cursoir (francês)
        cursor.execute(
            """INSERT INTO
                Disciplina (codigo, nome, carga_horaria, nome_professor)
                VALUES (?, ?, ?, ?)
            """,
            (   # dá pra entender que os valores estão sendo substituídos, né?
                disciplina.codigo,
                disciplina.nome,
                disciplina.carga_horaria,
                disciplina.nome_professor
            )
        )
        conexao.commit() # fecha
        
        return True
    

    def atualizar_disciplina(self, disciplina: DisciplinaModelo):    
        # checar se a disciplina existe    
        if self.validar.check_disciplina(disciplina.codigo):
            return False
        
        conexao = sqlite3.connect(self.caminho_banco)
        cursor = conexao.cursor()
        cursor.execute(
            """UPDATE Disciplina
               SET nome = ?, carga_horaria = ?, nome_professor = ?
               WHERE codigo = ?
            """,
            (
                disciplina.nome,
                disciplina.carga_horaria,
                disciplina.nome_professor,
                disciplina.codigo
            )
        )
        
        conexao.commit()
        return True
        
    
    