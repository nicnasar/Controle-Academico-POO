from database.banco_de_dados import BancoDeDados


class Disciplina:
    def __init__(self, codigo, nome, carga_horaria, nome_professor):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.nome_professor = nome_professor
        self.db = BancoDeDados()

    def cadastrar(self):
        """
        Cadastra a disciplina se não existir.
        """
        if self.db.buscar_disciplina_por_codigo(self.codigo):
            print(f"Disciplina com código '{self.codigo}' já existe.")
            return
        self.db.cadastrar_disciplina(self.codigo, self.nome, self.carga_horaria, self.nome_professor)

    @staticmethod
    def buscar(codigo):
        db = BancoDeDados()
        return db.buscar_disciplina_por_codigo(codigo)

    @staticmethod
    def listar():
        db = BancoDeDados()
        return db.listar_disciplinas()

    @staticmethod
    def remover(codigo):
        db = BancoDeDados()
        db.remover_disciplina(codigo)

