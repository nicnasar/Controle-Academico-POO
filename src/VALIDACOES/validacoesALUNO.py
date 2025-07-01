import sqlite3
from MODELOS.alunoMODELO import AlunoModelo


class Validar:
    
    
    def __init__(self, caminho_banco):
        self.caminho_banco = caminho_banco