#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno,NovaConsolidacaoGeralProfessor, UltimoStatusProfessor, UltimoStatusAlunos, NovaAgrecacaoIaAluno, NovaConsolidacaoGeralAluno, NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime


if __name__ == "__main__":

    Dados = Atividade.objects.all()

    for linha in Dados:
        if linha.municipio is not None:
            fixed = linha.municipio
            fixed = fixed.replace("RS-","")
            linha.municipio = fixed
            linha.save()
        