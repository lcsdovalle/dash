#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, UltimoStatusAlunos,NovaConsolidacaoGeralAluno, NovoIaAluno,NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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
    consolidado = PyCsv("lista-ticket")

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    dados = NovaConsolidacaoGeralAluno.objects.filter(data='2020-09-30')

    for item in dados:
        try:
            consolidado.add_row_csv([
                item.nome,
                item.nome_cre,
                item.inep,
                item.cre,
                item.municipio,
                item.menor_sete,
                item.maior_sete_menor_quatorze,
                item.maior_quatorze_menor_trinta,
                item.maior_trinta_menor_sessenta,
                item.maior_sessenta,
                item.ie,
                item.total_alunos,
                item.total_logaram,
                item.a_um_dia,
                item.a_dois_dias,
                item.a_tres_dias,
                item.a_quatro_dias,
                item.a_cinco_dias,
                item.a_seis_dias,
                item.a_sete_dias,
                item.a_nenhum_dia
            ])
        except Exception as e:
            print(e)



    