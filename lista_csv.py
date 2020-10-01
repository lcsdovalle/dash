#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, NovoIaAluno,NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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
    consolidado = PyCsv("consolidado_alunos")

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    alunos = Aluno.objects.all()
    escolas = Escola.objects.all()
    status = NovoStatusAluno.objects.all()
    todos_alunos = {}
    todos_professores = {}

    for escola in escolas:
        try:
            ie = NovoDispersaoAluno.objects.filter(inep=escola.inep,data='2020-09-28')
            iu = NovoIuAluno.objects.filter(inep=escola.inep,data='2020-09-28')
            ia = NovoIaAluno.objects.filter(inep=escola.inep,data='2020-09-28')
            ie = ie[0]
            iu = iu[0]
            ia = ia[0]
            ie,iu,ia

            consolidado.add_row_csv([
                escola.cre,
                escola.municipio,
                escola.inep,
                escola.nome,
                "{}%".format( round( (ia.total_logaram/ia.total_alunos) * 100) ),
                "{}%".format( round( ( (iu.a_quatro_dias+iu.a_cinco_dias+iu.a_cinco_dias) / (iu.a_um_dia+iu.a_dois_dias+iu.a_tres_dias+iu.a_quatro_dias+iu.a_cinco_dias+iu.a_seis_dias+iu.a_sete_dias) ) *100)  ),
                "{}%".format( round( ( (ie.menor_sete + ie.maior_sete_menor_quatorze) / (ie.menor_sete + ie.maior_sete_menor_quatorze + ie.maior_quatorze_menor_trinta + ie.maior_trinta_menor_sessenta + ie.maior_sessenta) ) *100 ) )
            ])
        except Exception as e:
            print(e)



    