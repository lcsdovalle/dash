#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno,NovaConsolidacaoGeralProfessor,NovoDispersaoProfessor,NovoIuProfessor,NovoIaPRofessor, NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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

    aluno_ie_inep = NovoDispersaoProfessor.objects.filter(data='2020-09-29')   
    for item in aluno_ie_inep:
        ie_aluno[item.inep] = {}
        ie_aluno[item.inep]['menor_sete'] = item.menor_sete
        ie_aluno[item.inep]['maior_sete_menor_quatorze'] = item.maior_sete_menor_quatorze
        ie_aluno[item.inep]['maior_quatorze_menor_trinta'] = item.maior_quatorze_menor_trinta
        ie_aluno[item.inep]['maior_trinta_menor_sessenta'] = item.maior_trinta_menor_sessenta
        ie_aluno[item.inep]['maior_sessenta'] = item.maior_sessenta
    
    aluno_ia_inep = NovoIaPRofessor.objects.filter(data='2020-09-29')
    for item in aluno_ia_inep:
        ia_aluno[item.inep] = {}
        ia_aluno[item.inep]['total_logaram'] = item.total_logaram
        ia_aluno[item.inep]['total_alunos'] = item.total_alunos


    aluno_iu_inep = NovoIuProfessor.objects.filter(data='2020-09-29') 
    for item in aluno_iu_inep:
        iu_aluno[item.inep] = {}
        iu_aluno[item.inep]['p_um_dia'] = item.p_um_dia
        iu_aluno[item.inep]['p_dois_dia'] = item.p_dois_dias
        iu_aluno[item.inep]['p_tres_dia'] = item.p_tres_dias
        iu_aluno[item.inep]['p_quatro_dia'] = item.p_quatro_dias
        iu_aluno[item.inep]['p_cinco_dia'] = item.p_cinco_dias
        iu_aluno[item.inep]['p_seis_dia'] = item.p_seis_dias
        iu_aluno[item.inep]['p_sete_dia'] = item.p_sete_dias
        iu_aluno[item.inep]['p_nenhum_dia'] = item.p_nenhum_dia

    for escola in escolas:
        Gravar = NovaConsolidacaoGeralProfessor()
        Gravar.nome = escola.nome
        Gravar.nome_cre = escola.nome_cre
        Gravar.inep = escola.inep
        Gravar.cre = escola.cre
        Gravar.municipio = escola.municipio

        indicadores = []
        
        try:
            dados_ie = ie_aluno[escola.inep]
            Gravar.menor_sete = dados_ie.get('menor_sete',0)
            Gravar.maior_sete_menor_quatorze = dados_ie.get('maior_sete_menor_quatorze',0)
            Gravar.maior_quatorze_menor_trinta = dados_ie.get('maior_quatorze_menor_trinta',0)
            Gravar.maior_trinta_menor_sessenta = dados_ie.get('maior_trinta_menor_sessenta',0)
            Gravar.maior_sessenta = dados_ie.get('maior_sessenta',0)
            indicadores.append(
                ( dados_ie.get('menor_sete',0) + dados_ie.get('maior_sete_menor_quatorze',0) ) / (dados_ie.get('menor_sete',0) + dados_ie.get('maior_sete_menor_quatorze',0) + dados_ie.get('maior_quatorze_menor_trinta',0) + dados_ie.get('maior_trinta_menor_sessenta',0) + dados_ie.get('maior_sessenta',0) ) * 100
            )

        except Exception as e:
            print(e)
            Gravar.menor_sete = 0
            Gravar.maior_sete_menor_quatorze = 0
            Gravar.maior_quatorze_menor_trinta = 0
            Gravar.maior_trinta_menor_sessenta = 0
            Gravar.maior_sessenta = 0
            indicadores.append(0)
        try:
            dados_ia = ia_aluno[escola.inep]
            Gravar.total_alunos = dados_ia.get('total_alunos',0)
            Gravar.total_logaram = dados_ia.get('total_logaram',0)
            indicadores.append( ( dados_ia.get('total_alunos',0) / dados_ia.get('total_alunos',0) ) * 100)
        except Exception as e:
            print(e)   
            Gravar.total_alunos = 0
            Gravar.total_logaram = 0
            indicadores.append(0)
        try:
            dados_iu = iu_aluno[escola.inep]
            Gravar.p_um_dia = dados_iu.get('p_um_dia')
            Gravar.p_dois_dias = dados_iu.get('p_dois_dia')
            Gravar.p_tres_dias = dados_iu.get('p_tres_dia')
            Gravar.p_quatro_dias = dados_iu.get('p_quatro_dia')
            Gravar.p_cinco_dias = dados_iu.get('p_cinco_dia')
            Gravar.p_seis_dias = dados_iu.get('p_seis_dia')
            Gravar.p_sete_dias = dados_iu.get('p_sete_dia')
            Gravar.p_nenhum_dia = dados_iu.get('p_nenhum_dia')
            indicadores.append(
               ( dados_iu.get('p_dois_dia') + dados_iu.get('p_tres_dia') + dados_iu.get('p_quatro_dia') + dados_iu.get('p_cinco_dia') + dados_iu.get('p_seis_dia') + dados_iu.get('p_sete_dia')) / (dados_iu.get('p_um_dia') + dados_iu.get('p_dois_dia') + dados_iu.get('p_tres_dia') + dados_iu.get('p_quatro_dia') + dados_iu.get('p_cinco_dia') + dados_iu.get('p_seis_dia') + dados_iu.get('p_sete_dia')) * 100
            )
        except Exception as e:
            print(e)    
            Gravar.p_um_dia =0
            Gravar.p_dois_dias = 0
            Gravar.p_tres_dias = 0
            Gravar.p_quatro_dias = 0
            Gravar.p_cinco_dias = 0
            Gravar.p_seis_dias = 0
            Gravar.p_sete_dias = 0
            Gravar.p_nenhum_dia = 0
            indicadores.append(0)
        indicadores.sort()

        fator_determinante_professor = indicadores[0]
        if fator_determinante_professor < 40:
            cor_prof = '1'
        elif fator_determinante_professor > 40 and fator_determinante_professor <70:
            cor_prof = '2'
        elif fator_determinante_professor >= 70:
            cor_prof = '3' 
        Gravar.status_professor = cor_prof
        Gravar.save()


    hoje = datetime.date.today().strftime('%Y-%m-%d')

    dados = NovaConsolidacaoGeralProfessor.objects.filter(data=hoje)
    muni_distintos = {}

    for item in dados:
        if item.municipio not in muni_distintos:
            muni_distintos[item.municipio] = {}
            muni_distintos[item.municipio] = 0
            muni_distintos[item.municipio] += int(item.status_professor)
        else:
            muni_distintos[item.municipio] += int(item.status_professor)

    for muni in muni_distintos:
        status = muni_distintos[muni]
        todos = NovaConsolidacaoGeralProfessor.objects.filter(municipio=muni)
        total = len(todos)

        resultado = int(status/total)
        for item in todos:
            item.status_professor = str(resultado)
            item.save()

    