
from MODELOS.alunoMODELO import AlunoModelo
from CONTROLE.controleALUNOS import ControleAluno
from DAO.alunoDAO import AlunoDao
from OUTROS.criarBANCO import CriarBanco

nome_banco = "src/controle_academico.db"

banco = CriarBanco(nome_banco)
banco._criar_banco()

aluno = AlunoModelo("maria", 34523, 12, "maria@gmail.com", "Rua dos passaros")

manipular_alunos = ControleAluno(AlunoDao(nome_banco))
manipular_alunos.cadastrar_aluno(aluno)


alunos = manipular_alunos.listar_alunos()

for aluno in alunos:
    print(aluno)