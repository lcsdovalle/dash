#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime


if __name__ == "__main__":

    # MONTA OS CSVS
    resultado = PyCsv("resultado")
    quantitativos = PyCsv("quantitativos")
    totais = PyCsv("totais")

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    alunos = AlunoEnsalado.objects.all()   
    escolas = Escola.objects.all()
    status = NovoStatusAluno.objects.all()
    for item in status:
        try:
            alunos_inep = alunos.filter(inep=item.inep)

            dt = datetime.date.today() - datetime.timedelta(days=2)
            n = NovaAgrecacaoIaAluno(
                data = dt.strftime('%Y-%m-%d'),
                inep = item.inep,
                cre = item.cre,
                municipio = item.municipio,
                total_ensalados = len(alunos_inep),
                total_logados = item.total_logaram
            )
            n.save()
        except Exception as e:
            print(e)



    