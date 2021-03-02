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
    Ultimo = NovaConsolidacaoGeralAluno.objects.filter(data=hoje)

    for linha in Ultimo:
        itemm = UltimoStatusAlunos.objects.filter(inep=linha.inep)
        if itemm.exists():
            item = itemm[0]
            linha.nome = item.nome
            linha.inep = item.inep
            linha.email = item.email
            linha.municipio = item.municipio
            linha.cre = item.cre
            linha.nome_cre = item.nome_cre  
            
            linha.ia = item.ia
            linha.ie = item.ie
            linha.iu = item.iu
            linha.status_aluno = item.status_aluno
            #IE
            linha.menor_sete = item.menor_sete
            linha.maior_sete_menor_quatorze = item.maior_sete_menor_quatorze
            linha.maior_quatorze_menor_trinta = item.maior_quatorze_menor_trinta
            linha.maior_trinta_menor_sessenta = item.maior_trinta_menor_sessenta
            linha.maior_sessenta = item.maior_sessenta
            
            
            #IU
            linha.a_um_dia = item.a_um_dia
            linha.a_dois_dias = item.a_dois_dias
            linha.a_tres_dias = item.a_tres_dias
            linha.a_quatro_dias = item.a_quatro_dias
            linha.a_cinco_dias = item.a_cinco_dias
            linha.a_seis_dias = item.a_seis_dias
            linha.a_sete_dias = item.a_sete_dias
            linha.a_nenhum_dia = item.a_nenhum_dia

            #IA
            linha.total_alunos = item.total_alunos
            linha.total_logaram = item.total_logaram
            
            linha.save()
