#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Professor,AcessosProfessor,Escola
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime

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

def botCarregarAcessoProfessores():

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    professores = Professor.objects.all()

    escolas = Escola.objects.all()
    escolastodas = {}
    for es in escolas:
        if es.inep not in escolastodas:
            escolastodas[es.inep] = {}
            escolastodas[es.inep]['cre'] = es.cre


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

    print("Professores carregados na memória")




    ########################
    # CONSTRÓI OS INTERVALOS 
    ########################
    hoje = datetime.datetime.today() - datetime.timedelta(days=1)
    inicio = datetime.datetime.today() - datetime.timedelta(days=1)
    intervalo_menor_sete_dias = {
        "inicio":inicio,
        "fim":hoje
        # "inicio": datetime.date.today() - datetime.timedelta(days=7),
        # "fim": datetime.date.today() - datetime.timedelta(days=1),
    }

  
  
    intervalos = {}
    intervalos['menor_sete'] = intervalo_menor_sete_dias

    reports = []

    ########################
    # PEGA OS DADOS DO GSUITE
    ########################
    trava = {} 
    quants = {}
    # print(intervalos)
    print("Começou a carregar reports do gsuite ")
    cont = 0  
    for label in intervalos: #por intervalo
        pageToken = True
        intervalo = intervalos[label]
        started = False
        while pageToken is not None:
            inicio = ""
            fim = ""
            
            if 'ultimo' not in intervalo:
                # inicio = "{}T00:01:00Z".format(intervalo['inicio'].strftime('%Y-%m-%d'))
                # fim = "{}T23:59:00Z".format(intervalo['fim'].strftime('%Y-%m-%d'))
                inicio = "{}T00:01:00Z".format('2020-06-01')
                fim = "{}T23:59:00Z".format('2021-01-26')
 
            if not started:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login',eventName='login_success',startTime=inicio,endTime=fim).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")
                    started = True
                except Exception as e:
                    continue  
            else:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login',eventName='login_success', maxResults=1000,startTime=inicio,endTime=fim,pageToken=pageToken).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")  
                except Exception as e:
                    continue  
            
            
            ########################
            # CONTABILIZA OS DADOS POR USUÁRIOS
            ########################
            print("{} carregados do gsuite".format(len(reports)))
            reports
            contabilizador = {}
           
            for r in reports:
                cont += len(reports)
                # print(f"{cont} items baixados")
                user = False
                identificacao_unica_usuario = r.get('actor').get('email') #pega o email
                data_acesso_usuario = r.get('id').get('time') # pega o time
                adata_acesso = data_acesso_usuario #.split('T')[0] # monta a data para comparação
                

                #verifica se é aluno ou professor
                if identificacao_unica_usuario in todos_professores:
                    user = todos_professores.get(identificacao_unica_usuario)
                    role = 'Professor'
                else:
                    continue
                
                # só processa se for aluno
                # agrega o as datas por email
                if user and role == 'Professor' and user['email']:
                    #// GRAVA NO BANCO
                    contabilizador[user['email']] = {
                            'inep':user['inep'],
                            'cre':user['cre'],
                            'municipio':user['municipio']
                        }
                    # trava[user['email']] = 'processado'

                    acesso = AcessosProfessor(
                            data                            = adata_acesso,
                            inep                            = user['inep'],
                            email                           = user['email'],
                            municipio                       = user['municipio'],
                            cre                             = user['cre']
                    )

                    acesso.save()
         
            reports = []