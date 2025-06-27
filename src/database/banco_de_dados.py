import sqlite3

class BancoDeDados:
    """
    Classe para gerenciar a conexão com o banco de dados SQLite.
    """

    def __init__(self, db_name='controle_academico.db'):

        # Inicializa a conexão com o banco de dados.
        # :param db_name: Nome do arquivo do banco de dados.

        self.db_name = db_name
        self.conexao = None

    def conectar(self):

        # Estabelece a conexão com o banco de dados.

        try:
            self.conexao = sqlite3.connect(self.db_name)
            print(f"Conexão com '{self.db_name}' estabelecida com sucesso.")
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao conectar ao banco de dados: {e}")

    def criar_banco(self):
        conexao = None
        # Cria o banco de dados e suas tabelas.

        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            print(f"Conexão com '{self.db_name}' estabelecida com sucesso.")

            # --- Tabela Disciplina ---
            # Adicionando campo professor
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Disciplina (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                carga_horaria INTEGER NOT NULL,
                professor TEXT NOT NULL
            );
            """)
            print("Tabela 'Disciplina' criada ou já existente.")

            conexao.commit()

        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao operar no banco de dados: {e}")
        finally:
            if conexao:
                conexao.close()
                print("Conexão com o banco de dados fechada.")

    def cadastrar_disciplina(self, codigo, nome, carga_horaria, professor):
        conexao = None
        # Cadastrar uma nova disciplina no banco de dados.
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            # Verifica se já existe disciplina com o mesmo código
            cursor.execute("SELECT 1 FROM Disciplina WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                print(f"Já existe uma disciplina com o código '{codigo}'.")
                return
            cursor.execute(
                """
                INSERT INTO Disciplina (codigo, nome, carga_horaria, professor)
                VALUES (?, ?, ?, ?)
                """,
                (codigo, nome, carga_horaria, professor)
            )
            conexao.commit()
            print(f"Disciplina '{nome}' cadastrada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao cadastrar disciplina: {e}")
        finally:
            if conexao:
                conexao.close()

    def atualizar_disciplina(self, codigo, nome=None, carga_horaria=None, professor=None):
        conexao = None
        # Atualiza os dados de uma disciplina existente, exceto o código.
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            # Busca os dados atuais
            cursor.execute("SELECT nome, carga_horaria, professor FROM Disciplina WHERE codigo = ?", (codigo,))
            row = cursor.fetchone()
            if not row:
                print(f"Disciplina com código '{codigo}' não encontrada.")
                return
            nome_atual, carga_horaria_atual, professor_atual = row
            # Mantém os valores atuais se o novo valor for None ou vazio
            nome_final = nome if nome not in (None, "") else nome_atual
            carga_horaria_final = carga_horaria if carga_horaria not in (None, "") else carga_horaria_atual
            professor_final = professor if professor not in (None, "") else professor_atual
            cursor.execute(
                """
                UPDATE Disciplina SET nome = ?, carga_horaria = ?, professor = ? WHERE codigo = ?
                """,
                (nome_final, carga_horaria_final, professor_final, codigo)
            )
            conexao.commit()
            print(f"Disciplina com código '{codigo}' atualizada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao atualizar disciplina: {e}")
        finally:
            if conexao:
                conexao.close()

    def remover_disciplina(self, codigo):
        conexao = None
        # Remove uma disciplina pelo código.
        
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM Disciplina WHERE codigo = ?", (codigo,))
            conexao.commit()
            print(f"Disciplina com código '{codigo}' removida (se existia).")
        except sqlite3.Error as e:
            print(f"Erro ao remover disciplina: {e}")
        finally:
            if conexao:
                conexao.close()

    def buscar_disciplina_por_codigo(self, codigo):
        conexao = None
        # Busca uma disciplina pelo código.
        # Retorna um dicionário com os dados ou None se não existir.
        
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, codigo, nome, carga_horaria, professor FROM Disciplina WHERE codigo = ?",
                (codigo,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'codigo': row[1],
                    'nome': row[2],
                    'carga_horaria': row[3],
                    'professor': row[4]
                }
            return None
        except sqlite3.Error as e:
            print(f"Erro ao buscar disciplina: {e}")
            return None
        finally:
            if conexao:
                conexao.close()

    def listar_disciplinas(self):
        conexao = None
        # Lista todas as disciplinas cadastradas.
        # Retorna uma lista de dicionários.
        
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            cursor.execute("SELECT id, codigo, nome, carga_horaria, professor FROM Disciplina")
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'codigo': row[1],
                    'nome': row[2],
                    'carga_horaria': row[3],
                    'professor': row[4]
                }
                for row in rows
            ]
        except sqlite3.Error as e:
            print(f"Erro ao listar disciplinas: {e}")
            return []
        finally:
            if conexao:
                conexao.close()
