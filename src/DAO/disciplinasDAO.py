import sqlite3

#    PASTA   arqUIVO                  ClaSse
from MODELOS.disciplinasMODELO import DisciplinaModelo
from VALIDACOES.validacoesDISCIPLINAS import Validar

# TODO: fazer funções para checar valores, deixar em pasta separada


class DisciplinaDao:
    def __init__(self, caminho_banco):
        # função para conectar em um banco geral, sem precisar ficar escrevendo tudo toda vez
        self.caminho_banco = caminho_banco
        self.validar = Validar(caminho_banco)
            
    def cadastrar_disciplina(self, disciplina: DisciplinaModelo):
        
        if self.validar.check_disciplina(disciplina.codigo):
            return "Não foi possível cadastrar a disciplina, pois possui o mesmo código de uma já existente."
        # colocar futuramente qual disciplina é essa
        
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
        
        return "Disciplina cadastrada com sucesso!"
    
    
    # def atualizar_disciplina(self, disciplina: DisciplinaModelo):
        
        
        
    
    