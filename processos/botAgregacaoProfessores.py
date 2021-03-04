#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import Turmas,NovoDispersaoProfessor,NovaConsolidacaoGeralProfessor, NovoIaPRofessor, NovoStatusProfessor, NovoIuProfessor, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
from pylib.MyBigQuery import Stream
import datetime
from google.cloud import bigquery
stream = Stream('getedu-api-293018')
stream.set_client(bigquery.Client()).set_dataset('riograndedosul').set_table('consolidados_professores')

# rowteste = [
#     {"cre":3131312}
# ]
# stream.inserir(rowteste)
# stream.set_sql( "TRUNCATE TABLE {}".format(stream.get_tableid()) )
# stream.execute_query()
# stream

escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly', 
        'https://www.googleapis.com/auth/admin.reports.audit.readonly',
    ]
service_class = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@educar.rs.gov.br"
    ).getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

def botAgregacaoProfessores():

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    professores = Professor.objects.all()
    escolas = Escola.objects.all()

    todos_professores = {}
    todos_professores_inep = {}

    for professor in professores:
        for inep in professor.inep.split(','):
            if inep not in todos_professores_inep:
                todos_professores_inep[inep] = 1
            else:
                todos_professores_inep[inep] += 1

        todos_professores[professor.email] = {}
        todos_professores[professor.email]['email'] = professor.email
        todos_professores[professor.email]['inep'] = professor.inep
        todos_professores[professor.email]['municipio'] = professor.municipio
        todos_professores[professor.email]['cre'] = professor.cre

    ########################
    # CONSTRÓI OS INTERVALOS 
    ########################

    hoje = datetime.datetime.today() - datetime.timedelta(days=1)

    interval = [
        hoje - datetime.timedelta(days=6),
        hoje - datetime.timedelta(days=5),
        hoje - datetime.timedelta(days=4),
        hoje - datetime.timedelta(days=3),
        hoje - datetime.timedelta(days=2),
        hoje - datetime.timedelta(days=1),
        hoje,
        
    ]
    
    intervals = list(map(toStr,interval))
    intervalo_menor_sete_dias = {
        "inicio": hoje - datetime.timedelta(days=6),
        "fim": hoje,
    }
    intervalo_maior_sete_menor_quartorze = {
        "inicio": hoje - datetime.timedelta(days=14),
        "fim": hoje - datetime.timedelta(days=7),
    }
    intervalo_maior_quatorze_menor_trinta = {
        "inicio": hoje - datetime.timedelta(days=29),
        "fim": hoje - datetime.timedelta(days=15),
    }
    intervalo_maior_trinta_menor_sessenta = {
        "inicio": hoje - datetime.timedelta(days=59),
        "fim": hoje - datetime.timedelta(days=30),
    }
    intervalo_maior_sessenta = {
        "ultimo": datetime.date.today() - datetime.timedelta(days=59),
    }
  
    intervalos = {}
    intervalos['menor_sete'] = intervalo_menor_sete_dias
    intervalos['maior_sete_menor_quatorze'] = intervalo_maior_sete_menor_quartorze
    intervalos['maior_quatorze_menor_trinta'] = intervalo_maior_quatorze_menor_trinta
    intervalos['maior_trinta_menor_sessenta'] = intervalo_maior_trinta_menor_sessenta
    intervalos['maior_sessenta'] = intervalo_maior_sessenta
    # print(intervalos)

    ########################
    # PEGA OS DADOS DO GSUITE
    ########################

    trava = {} 
    quants = {}
    reports = []

    for label in intervalos: #por intervalo
        pageToken = True
        intervalo = intervalos[label]
        started = False
        while pageToken is not None:
            inicio = ""
            fim = ""

            if 'ultimo' not in intervalo:
                inicio = "{}T00:00:00Z".format(intervalo['inicio'].strftime('%Y-%m-%d'))
                fim = "{}T23:59:00Z".format(intervalo['fim'].strftime('%Y-%m-%d'))
            else:
                inicio = "2020-06-01T00:00:00Z"
                fim = "{}T23:59:00Z".format(intervalo['ultimo'].strftime('%Y-%m-%d'))
 
            if not started:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk73768f3m',applicationName='login',startTime=inicio,endTime=fim).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")
                    started = True 
                except Exception as e:
                    continue 
            else:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk73768f3m',applicationName='login', maxResults=1000,startTime=inicio,endTime=fim,pageToken=pageToken).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")  
                except Exception as e:
                    continue

            # > um recuo
            ########################
            # CONTABILIZA OS DADOS POR USUÁRIOS
            ########################
            reports
            contabilizador = {}  
            for r in reports:
                user = False
                identificacao_unica_usuario = r.get('actor').get('email') #pega o email
                data_acesso_usuario = r.get('id').get('time') # pega o time
                adata_acesso = data_acesso_usuario.split('T')[0] # monta a data para comparação
                

                #verifica se é aluno ou professor
                if identificacao_unica_usuario in todos_professores:    
                    user = todos_professores.get(identificacao_unica_usuario)
                    role='Professor'
                else:
                    continue
                
                # só processa se for aluno
                # agrega o as datas por email
                if user and user['email'] not in contabilizador and user['email'] not in trava:
                    contabilizador[user['email']] = {
                            'inep':user['inep'],
                            'cre':user['cre'],
                            'municipio':user['municipio'],
                            'dias':[]
                        }
                    trava[user['email']] = 'processado'

                if user['email'] in contabilizador:
                    if adata_acesso not in contabilizador[user['email']]['dias'] and adata_acesso in intervals:
                        contabilizador[user['email']]['dias'].append(str(adata_acesso))     
                    
            ########################
            # CONTABILIZA OS DADOS POR INEP
            ########################
            for email in contabilizador:
                dados = contabilizador[email]       
                for inep in dados['inep'].split(','):
                    if inep not in quants:
                        quants[inep] = {}
                        quants[inep][label] = 0
                        quants[inep][label] += 1
                        quants[inep]['cre'] = dados['cre']
                        quants[inep]['municipio'] = dados['municipio']
                        quants[inep]['total'] = 0
                        quants[inep]['total'] += 1
                        quants[inep]['total_geral'] = todos_professores_inep[inep]
                        
                        quants[inep]['p_um_dia'] = 1 if len(dados['dias']) == 1 else 0
                        quants[inep]['p_dois_dia'] = 1 if len(dados['dias']) == 2 else 0
                        quants[inep]['p_tres_dia'] = 1 if len(dados['dias']) == 3 else 0
                        quants[inep]['p_quatro_dia'] = 1 if len(dados['dias']) == 4 else 0
                        quants[inep]['p_cinco_dia'] = 1 if len(dados['dias']) == 5 else 0
                        quants[inep]['p_seis_dia'] = 1 if len(dados['dias']) == 6 else 0
                        quants[inep]['p_sete_dia'] = 1 if len(dados['dias']) == 7 else 0
                        quants[inep]['p_nenhum_dia'] = 1 if len(dados['dias']) == 0 else 0

                    else:
                        if label not in quants[inep]:
                            quants[inep][label] = 0 
                        quants[inep][label] += 1
                        quants[inep]['total'] += 1

                        if label == 'menor_sete':
                            quants[inep]['p_um_dia'] += 1 if len(dados['dias']) == 1 else 0
                            quants[inep]['p_dois_dia'] += 1 if len(dados['dias']) == 2 else 0
                            quants[inep]['p_tres_dia'] += 1 if len(dados['dias']) == 3 else 0
                            quants[inep]['p_quatro_dia'] += 1 if len(dados['dias']) == 4 else 0
                            quants[inep]['p_cinco_dia'] += 1 if len(dados['dias']) == 5 else 0
                            quants[inep]['p_seis_dia'] += 1 if len(dados['dias']) == 6 else 0
                            quants[inep]['p_sete_dia'] += 1 if len(dados['dias']) == 7 else 0
                            quants[inep]['p_nenhum_dia'] += 1 if len(dados['dias']) == 0 else 0

            started=False
            reports = []

            # >> dois recuos
            ########################
            # GRAVA NO BANCO DE DADOS
            ########################
            hoje = datetime.date.today() #- datetime.timedelta(days=1)
            hoje = hoje.strftime('%Y-%m-%d')
            for inep in quants:
                data = quants[inep]
                escola = escolas.get(inep=inep)
                try:
                    Gravar = NovaConsolidacaoGeralProfessor()
                    Gravar.data = hoje
                    Gravar.nome = escola.nome
                    Gravar.nome_cre = escola.nome_cre
                    Gravar.inep = escola.inep
                    Gravar.cre = escola.cre
                    Gravar.municipio = escola.municipio

                    Gravar.menor_sete = data.get('menor_sete',0)
                    Gravar.maior_sete_menor_quatorze = data.get('maior_sete_menor_quatorze',0)
                    Gravar.maior_quatorze_menor_trinta = data.get('maior_quatorze_menor_trinta',0)
                    Gravar.maior_trinta_menor_sessenta = data.get('maior_trinta_menor_sessenta',0)
                    Gravar.maior_sessenta = data.get('maior_sessenta',0)

                    #IU
                    Gravar.p_um_dia = data.get('p_um_dia',0)
                    Gravar.p_dois_dias = data.get('p_dois_dia',0)
                    Gravar.p_tres_dias = data.get('p_tres_dia',0)
                    Gravar.p_quatro_dias = data.get('p_quatro_dia',0)
                    Gravar.p_cinco_dias = data.get('p_cinco_dia',0)
                    Gravar.p_seis_dias = data.get('p_seis_dia',0)
                    Gravar.p_sete_dias = data.get('p_sete_dia',0)
                    Gravar.p_nenhum_dia = data.get('p_sete_dia',0)
                    
                    
                    #IA
                    Gravar.total_alunos = data['total_geral']
                    Gravar.total_logaram = total_logaram = data['total']
                    Gravar.save()


                except Exception as e:
                    print(e) 