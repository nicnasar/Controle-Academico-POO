
from OUTROS.criarBANCO import CriarBanco

from MODELOS.disciplinasMODELO import DisciplinaModelo
from MODELOS.alunoMODELO import AlunoModelo

from DAO.disciplinasDAO import DisciplinaDao
from DAO.alunoDAO import AlunoDao

from CONTROLE.controleDISCIPLINAS import ControleDisciplina
from CONTROLE.controleALUNOS import ControleAluno


nome_banco = "src/controle_academico.db"

banco = CriarBanco(nome_banco)

# aluno = AlunoModelo("maria", 34523, 12, "maria@gmail.com", "Rua dos passaros")

# manipular_alunos = ControleAluno(AlunoDao(nome_banco))
# manipular_alunos.cadastrar_aluno(aluno)

# criar instância disciplina

disciplina0 = DisciplinaModelo(85, "Soco", 7, "macrcekai")
disciplina1 = DisciplinaModelo(68, "FELICIDADE", None, None)

manipular_disciplinas = ControleDisciplina(DisciplinaDao(nome_banco))

# manipular_disciplinas.cadastrar_disciplina(disciplina0)
manipular_disciplinas.atualizar_disciplina(disciplina1)

"""
alunos = manipular_alunos.listar_alunos()

for aluno in alunos:
    print(aluno)
"""