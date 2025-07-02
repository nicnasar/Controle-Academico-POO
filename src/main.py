
from OUTROS.criarBANCO import CriarBanco

from MODELOS.disciplinasMODELO import DisciplinaModelo
from MODELOS.alunoMODELO import AlunoModelo
from MODELOS.matriculasMODELO import MatriculaModelo

from DAO.disciplinasDAO import DisciplinaDao
from DAO.alunoDAO import AlunoDao
from DAO.matriculasDAO import MatriculaDao

from CONTROLE.controleDISCIPLINAS import ControleDisciplina
from CONTROLE.controleALUNOS import ControleAluno
from CONTROLE.controleMATRICULAS import ControleMatricula

nome_banco = "controle_academico.db"

banco = CriarBanco(nome_banco)

# consertar função cadastrar aluno
# aluna = AlunoModelo("Victória", 16965065737, 21, "vickallas@gmail.com", 0000000)

manipular_alunos = ControleAluno(AlunoDao(nome_banco))

manipular_matriculas = ControleMatricula(MatriculaDao(nome_banco))
# manipular_alunos.cadastrar_aluno(aluna)

# criar instância disciplina

# disciplina0 = DisciplinaModelo(9, None, None, "Josias")
# disciplina1 = DisciplinaModelo(7, "Cálculo I", 180, "Lagrange")

manipular_disciplinas = ControleDisciplina(DisciplinaDao(nome_banco))

# manipular_disciplinas.atualizar_disciplina(disciplina0)

# manipular_disciplinas.deletar_disciplina(disciplina0)

# manipular_disciplinas.cadastrar_disciplina(disciplina1)

# manipular_disciplinas.listar_dados()

matricula = MatriculaModelo(1, 16965065737, "02/07", "11:21")

manipular_matriculas.cancelar_matricula(matricula)
manipular_matriculas.listar_dados_csv()

"""
alunos = manipular_alunos.listar_alunos()

for aluno in alunos:
    print(aluno)
"""