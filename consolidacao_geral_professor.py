#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno,UltimoStatusProfessor ,NovaConsolidacaoGeralProfessor,NovoDispersaoProfessor,NovoIuProfessor,NovoIaPRofessor, NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime

if __name__ == "__main__":

    # MONTA OS CSVS

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR

    escolas = Escola.objects.all()
    ie_aluno = {}
    ia_aluno = {}
    iu_aluno = {}
    ontem = datetime.datetime.today() #- datetime.timedelta(days=1)
    ontem = ontem.strftime('%Y-%m-%d')
    #IE
    aluno_ie_inep = NovoDispersaoProfessor.objects.filter(data=ontem)   
    for item in aluno_ie_inep:
        ie_aluno[item.inep] = {}
        ie_aluno[item.inep]['menor_sete'] = item.menor_sete
        ie_aluno[item.inep]['maior_sete_menor_quatorze'] = item.maior_sete_menor_quatorze
        ie_aluno[item.inep]['maior_quatorze_menor_trinta'] = item.maior_quatorze_menor_trinta
        ie_aluno[item.inep]['maior_trinta_menor_sessenta'] = item.maior_trinta_menor_sessenta
        ie_aluno[item.inep]['maior_sessenta'] = item.maior_sessenta
        ie_aluno[item.inep]['ie'] = ( 
                item.menor_sete + 
                item.maior_sete_menor_quatorze 
            ) / (
                item.menor_sete + 
                item.maior_sete_menor_quatorze  + 
                item.maior_quatorze_menor_trinta + 
                item.maior_trinta_menor_sessenta + 
                item.maior_sessenta 
            ) * 100 or 0
    #IA
    aluno_ia_inep = NovoIaPRofessor.objects.filter(data=ontem)
    for item in aluno_ia_inep:
        ia_aluno[item.inep] = {}
        ia_aluno[item.inep]['total_logaram'] = item.total_logaram
        ia_aluno[item.inep]['total_alunos'] = item.total_alunos
        ia_aluno[item.inep]['ia'] =  ( item.total_logaram / item.total_alunos ) * 100


    aluno_iu_inep = NovoIuProfessor.objects.filter(data=ontem) 
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
        iu_aluno[item.inep]['iu'] = (
                ( 
                    item.p_dois_dias + 
                    item.p_tres_dias + 
                    item.p_quatro_dias + 
                    item.p_cinco_dias + 
                    item.p_seis_dias + 
                    item.p_sete_dias
                ) / (
                    item.p_um_dia+ 
                    item.p_dois_dias + 
                    item.p_tres_dias + 
                    item.p_quatro_dias + 
                    item.p_cinco_dias + 
                    item.p_seis_dias + 
                    item.p_sete_dias
                ) * 100
        )
    d = datetime.date.today() # - datetime.timedelta(days=1)
    d = d.strftime('%Y-%m-%d')
    for escola in escolas:
        Gravar = NovaConsolidacaoGeralProfessor()
        Gravar.nome = escola.nome
        Gravar.nome_cre = escola.nome_cre
        Gravar.inep = escola.inep
        Gravar.cre = escola.cre
        Gravar.municipio = escola.municipio
        Gravar.data = d
        indicadores = []
        
        #IE 
        try:
            dados_ie = ie_aluno[escola.inep]
            ie = dados_ie.get('ie',0)
            Gravar.menor_sete = dados_ie.get('menor_sete',0)
            Gravar.maior_sete_menor_quatorze = dados_ie.get('maior_sete_menor_quatorze',0)
            Gravar.maior_quatorze_menor_trinta = dados_ie.get('maior_quatorze_menor_trinta',0)
            Gravar.maior_trinta_menor_sessenta = dados_ie.get('maior_trinta_menor_sessenta',0)
            Gravar.maior_sessenta = dados_ie.get('maior_sessenta',0)
            Gravar.ie = int(dados_ie.get('ie',0))
        except Exception as e:
            print(e)
           
            Gravar.menor_sete = 0
            Gravar.maior_sete_menor_quatorze = 0
            Gravar.maior_quatorze_menor_trinta = 0
            Gravar.maior_trinta_menor_sessenta = 0
            Gravar.maior_sessenta = 0
            Gravar.ie = 0
            
        #IA
        try:
            dados_ia = ia_aluno[escola.inep]
            ia = dados_ia.get('ia',0)
            Gravar.total_alunos = dados_ia.get('total_alunos',0)
            Gravar.total_logaram = dados_ia.get('total_logaram',0)
            Gravar.ia = int(dados_ia.get('ia',0))
        except Exception as e:
            print(e)   
           
            Gravar.total_alunos = 0
            Gravar.total_logaram = 0
            Gravar.ia = 0
       
        
        #IU
        try:
            dados_iu = iu_aluno[escola.inep]
            iu = dados_iu.get('iu',0)
            Gravar.p_um_dia = dados_iu.get('p_um_dia')
            Gravar.p_dois_dias = dados_iu.get('p_dois_dia')
            Gravar.p_tres_dias = dados_iu.get('p_tres_dia')
            Gravar.p_quatro_dias = dados_iu.get('p_quatro_dia')
            Gravar.p_cinco_dias = dados_iu.get('p_cinco_dia')
            Gravar.p_seis_dias = dados_iu.get('p_seis_dia')
            Gravar.p_sete_dias = dados_iu.get('p_sete_dia')
            Gravar.p_nenhum_dia = dados_iu.get('p_nenhum_dia')
            Gravar.iu = int(dados_iu.get('iu',0))
        except Exception as e:
            print(e)    
          
            Gravar.p_um_dia = 0
            Gravar.p_dois_dias =0
            Gravar.p_tres_dias = 0
            Gravar.p_quatro_dias = 0
            Gravar.p_cinco_dias = 0
            Gravar.p_seis_dias = 0
            Gravar.p_sete_dias = 0
            Gravar.p_nenhum_dia = 0
            Gravar.iu = 0
        

        Gravar.status_professor = 0
        Gravar.save()


    hoje = datetime.date.today()# - datetime.timedelta(days=1)
    hoje = hoje.strftime('%Y-%m-%d')
    
    dados = NovaConsolidacaoGeralProfessor.objects.filter(data=hoje)
    muni_distintos = {}

    for item in dados:
        if item.municipio not in muni_distintos:
            muni_distintos[item.municipio] = {}
            muni_distintos[item.municipio]['ia'] = 0
            muni_distintos[item.municipio]['ie'] = 0
            muni_distintos[item.municipio]['iu'] = 0
            muni_distintos[item.municipio]['ia'] += int(item.ia)
            muni_distintos[item.municipio]['ie'] += int(item.ie)
            muni_distintos[item.municipio]['iu'] += int(item.iu)
        else:
            muni_distintos[item.municipio]['ia'] += int(item.ia)
            muni_distintos[item.municipio]['ie'] += int(item.ie)
            muni_distintos[item.municipio]['iu'] += int(item.iu)

    for muni in muni_distintos:
        
        todos = NovaConsolidacaoGeralProfessor.objects.filter(municipio=muni, data=hoje)
        total = len(todos)

        indicadores = []
        status = muni_distintos[muni]
        
        indicadores.append(status.get('ia',0) / total) 
        indicadores.append(status.get('ie',0) / total) 
        indicadores.append(status.get('iu',0) / total) 
        indicadores.sort()

        try:
            fator_determinante = indicadores[0]
            if fator_determinante < 40:
                cor = '1'
            elif fator_determinante > 40 and fator_determinante <70:
                cor = '2'
            elif fator_determinante >= 70:
                cor = '3' 

            cor
            for item in todos:
                item.status_professor = str(cor)
                item.save()
        except:
            pass
    Ultimo = NovaConsolidacaoGeralProfessor.objects.filter(data=hoje)

    for linha in Ultimo:
        item = UltimoStatusProfessor.objects.get_or_create(inep=linha.inep)[0]
        item.nome = linha.nome
        item.inep = linha.inep
        item.email = linha.email
        item.municipio = linha.municipio
        item.cre = linha.cre
        item.nome_cre = linha.nome_cre  
        
        item.ia = linha.ia
        item.ie = linha.ie
        item.iu = linha.iu
        item.status_professor = linha.status_professor
        #IE
        item.menor_sete = linha.menor_sete
        item.maior_sete_menor_quatorze = linha.maior_sete_menor_quatorze
        item.maior_quatorze_menor_trinta = linha.maior_quatorze_menor_trinta
        item.maior_trinta_menor_sessenta = linha.maior_trinta_menor_sessenta
        item.maior_sessenta = linha.maior_sessenta
        
        
        #IU
        item.p_um_dia = linha.p_um_dia
        item.p_dois_dias = linha.p_dois_dias
        item.p_tres_dias = linha.p_tres_dias
        item.p_quatro_dias = linha.p_quatro_dias
        item.p_cinco_dias = linha.p_cinco_dias
        item.p_seis_dias = linha.p_seis_dias
        item.p_sete_dias = linha.p_sete_dias
        item.p_nenhum_dia = linha.p_nenhum_dia

        #IA
        item.total_alunos = linha.total_alunos
        item.total_logaram = linha.total_logaram
        
        item.save()
