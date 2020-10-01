#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, NovaAgrecacaoIaAluno, NovaConsolidacaoGeralAluno, NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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

    escolas = Escola.objects.all()
    ie_aluno = {}
    ia_aluno = {}
    iu_aluno = {}

    aluno_ie_inep = NovoDispersaoAluno.objects.filter(data='2020-09-28')   
    for item in aluno_ie_inep:
        ie_aluno[item.inep] = {}
        ie_aluno[item.inep]['menor_sete'] = item.menor_sete
        ie_aluno[item.inep]['maior_sete_menor_quatorze'] = item.maior_sete_menor_quatorze
        ie_aluno[item.inep]['maior_quatorze_menor_trinta'] = item.maior_quatorze_menor_trinta
        ie_aluno[item.inep]['maior_trinta_menor_sessenta'] = item.maior_trinta_menor_sessenta
        ie_aluno[item.inep]['maior_sessenta'] = item.maior_sessenta
    
    aluno_ia_inep = NovoIaAluno.objects.filter(data='2020-09-28')
    for item in aluno_ia_inep:
        ia_aluno[item.inep] = {}
        ia_aluno[item.inep]['total_logaram'] = item.total_logaram
        ia_aluno[item.inep]['total_alunos'] = item.total_alunos


    aluno_iu_inep = NovoIuAluno.objects.filter(data='2020-09-28') 
    for item in aluno_iu_inep:
        iu_aluno[item.inep] = {}
        iu_aluno[item.inep]['a_um_dia'] = item.a_um_dia
        iu_aluno[item.inep]['a_dois_dia'] = item.a_dois_dias
        iu_aluno[item.inep]['a_tres_dia'] = item.a_tres_dias
        iu_aluno[item.inep]['a_quatro_dia'] = item.a_quatro_dias
        iu_aluno[item.inep]['a_cinco_dia'] = item.a_cinco_dias
        iu_aluno[item.inep]['a_seis_dia'] = item.a_seis_dias
        iu_aluno[item.inep]['a_sete_dia'] = item.a_sete_dias
        iu_aluno[item.inep]['a_nenhum_dia'] = item.a_nenhum_dia
    d = datetime.date.today() - datetime.timedelta(days=2)
    d = d.strftime('%Y-%m-%d')
    for escola in escolas:
        Gravar = NovaConsolidacaoGeralAluno()
        Gravar.nome = escola.nome
        Gravar.nome_cre = escola.nome_cre
        Gravar.inep = escola.inep
        Gravar.cre = escola.cre
        Gravar.municipio = escola.municipio
        Gravar.data = d
        
        try:
            dados_ie = ie_aluno[escola.inep]
            Gravar.menor_sete = dados_ie.get('menor_sete',0)
            Gravar.maior_sete_menor_quatorze = dados_ie.get('maior_sete_menor_quatorze',0)
            Gravar.maior_quatorze_menor_trinta = dados_ie.get('maior_quatorze_menor_trinta',0)
            Gravar.maior_trinta_menor_sessenta = dados_ie.get('maior_trinta_menor_sessenta',0)
            Gravar.maior_sessenta = dados_ie.get('maior_sessenta',0)

        except Exception as e:
            print(e)
            Gravar.menor_sete = 0
            Gravar.maior_sete_menor_quatorze = 0
            Gravar.maior_quatorze_menor_trinta = 0
            Gravar.maior_trinta_menor_sessenta = 0
            Gravar.maior_sessenta = 0
        

        try:
            total_ensalados = NovaAgrecacaoIaAluno.objects.get(inep=escola.inep) 

            dados_ia = ia_aluno[escola.inep]
            Gravar.total_alunos = total_ensalados.get(total_ensalados,0)
            Gravar.total_logaram = dados_ia.get('total_logaram',0)
        except Exception as e:
            print(e)   
            Gravar.total_alunos = 0
            Gravar.total_logaram = 0
        
        try:
            dados_iu = iu_aluno[escola.inep]
            Gravar.a_um_dia = dados_iu.get('a_um_dia')
            Gravar.a_dois_dias = dados_iu.get('a_dois_dia')
            Gravar.a_tres_dias = dados_iu.get('a_tres_dia')
            Gravar.a_quatro_dias = dados_iu.get('a_quatro_dia')
            Gravar.a_cinco_dias = dados_iu.get('a_cinco_dia')
            Gravar.a_seis_dias = dados_iu.get('a_seis_dia')
            Gravar.a_sete_dias = dados_iu.get('a_sete_dia')
            Gravar.a_nenhum_dia = dados_iu.get('a_nenhum_dia')
        except Exception as e:
            print(e)    
            Gravar.a_um_dia = 0
            Gravar.a_dois_dias =0
            Gravar.a_tres_dias = 0
            Gravar.a_quatro_dias = 0
            Gravar.a_cinco_dias = 0
            Gravar.a_seis_dias = 0
            Gravar.a_sete_dias = 0
            Gravar.a_nenhum_dia = 0
        Gravar.save()
        print(Gravar.inep)


    