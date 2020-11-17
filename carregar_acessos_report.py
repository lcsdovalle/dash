#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import AcessosAlunos, Aluno, Escola
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

if __name__ == "__main__":

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    alunos = Aluno.objects.all()

    escolas = Escola.objects.all()
    escolastodas = {}
    for es in escolas:
        if es.inep not in escolastodas:
            escolastodas[es.inep] = {}
            escolastodas[es.inep]['cre'] = es.cre


    todos_alunos = {}
    todos_alunos_por_inep = {}
    for aluno in alunos:
        if aluno.inep not in todos_alunos_por_inep:
            todos_alunos_por_inep[aluno.inep] = 1
        else:
            todos_alunos_por_inep[aluno.inep] += 1


        todos_alunos[aluno.email] = {}
        todos_alunos[aluno.email]['email'] = aluno.email
        todos_alunos[aluno.email]['inep'] = aluno.inep
        todos_alunos[aluno.email]['municipio'] = aluno.municipio
        todos_alunos[aluno.email]['cre'] = aluno.cre
        todos_alunos[aluno.email]['ultimo_acesso'] = aluno.ultimo_acesso

    print("Alunos carregados na memória")




    ########################
    # CONSTRÓI OS INTERVALOS 
    ########################
    hoje = datetime.datetime.today()   - datetime.timedelta(days=21)
    # hoje = datetime.datetime.today()   - datetime.timedelta(days=1)
    intervalo_menor_sete_dias = {
        "inicio": datetime.datetime.strptime("2020-06-01",'%Y-%m-%d'),
        "fim": hoje ,
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
    print(intervalos)
    print("Começou a carregar reports do gsuite ")
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
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login',startTime=inicio,endTime=fim).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")
                    started = True
                except Exception as e:
                    continue  
            else:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login', maxResults=1000,startTime=inicio,endTime=fim,pageToken=pageToken).execute()
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
                user = False
                identificacao_unica_usuario = r.get('actor').get('email') #pega o email
                data_acesso_usuario = r.get('id').get('time') # pega o time
                adata_acesso = data_acesso_usuario #.split('T')[0] # monta a data para comparação
                

                #verifica se é aluno ou professor
                if identificacao_unica_usuario in todos_alunos:
                    user = todos_alunos.get(identificacao_unica_usuario)
                    role = 'Aluno'
                else:
                    continue
                
                # só processa se for aluno
                # agrega o as datas por email
                if user and role == 'Aluno' and user['email']:
                    #// GRAVA NO BANCO
                    contabilizador[user['email']] = {
                            'inep':user['inep'],
                            'cre':user['cre'],
                            'municipio':user['municipio']
                        }
                    # trava[user['email']] = 'processado'

                    acesso = AcessosAlunos(
                            data                            = adata_acesso,
                            inep                            = user['inep'],
                            email                           = user['email'],
                            municipio                       = user['municipio'],
                            cre                             = user['cre']

                    )

                    acesso.save()
            reports = []