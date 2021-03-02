#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, UltimoStatusAlunos, NovaAgrecacaoIaAluno, NovaConsolidacaoGeralAluno, NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime


if __name__ == "__main__":


    hoje = '2020-12-13'
    Ultimo = Escola.objects.all()

    for linha in Ultimo:
        itemm = UltimoStatusAlunos.objects.filter(inep=linha.inep)
        if not itemm.exists() or itemm.exists() is None:
            nova = UltimoStatusAlunos()

            nova.nome = linha.nome
            nova.inep = linha.inep
            nova.email = linha.email
            nova.municipio = linha.municipio
            nova.cre = linha.cre
            nova.nome_cre = linha.nome_cre  
            
            nova.ia = 0
            nova.ie = 0
            nova.iu = 0
            nova.status_aluno = 0
            #IE
            nova.menor_sete = 0
            nova.maior_sete_menor_quatorze = 0
            nova.maior_quatorze_menor_trinta = 0
            nova.maior_trinta_menor_sessenta = 0
            nova.maior_sessenta = 0
            
            
            #IU
            nova.a_um_dia = 0
            nova.a_dois_dias = 0
            nova.a_tres_dias = 0
            nova.a_quatro_dias = 0
            nova.a_cinco_dias = 0
            nova.a_seis_dias = 0
            nova.a_sete_dias = 0
            nova.a_nenhum_dia = 0

            #IA
            nova.total_alunos = 0
            nova.total_logaram =0
            
            nova.save()
