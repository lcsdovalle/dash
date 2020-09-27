#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime



escopos = [
        # 'https://www.googleapis.com/auth/classroom.courses',
        # 'https://www.googleapis.com/auth/classroom.courses.readonly',
        # 'https://www.googleapis.com/auth/classroom.rosters',
        # 'https://www.googleapis.com/auth/classroom.profile.emails',
        # 'https://www.googleapis.com/auth/classroom.profile.photos',
        # 'https://www.googleapis.com/auth/admin.reports.usage.readonly',
        'https://www.googleapis.com/auth/admin.reports.audit.readonly',
        # 'https://www.googleapis.com/auth/classroom.coursework.students',
        # 'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        # 'https://www.googleapis.com/auth/classroom.coursework.me',
        # 'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    ]
# service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    # MONTA OS CSVS
    resultado = PyCsv("resultado")
    quantitativos = PyCsv("quantitativos")
    totais = PyCsv("totais")

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    alunos = Aluno.objects.all()
    professores = Professor.objects.all()
    escolas = Escola.objects.all()
    todos_alunos = {}
    todos_professores = {}
    for aluno in alunos:
        todos_alunos[aluno.email] = {}
        todos_alunos[aluno.email]['email'] = aluno.email
        todos_alunos[aluno.email]['inep'] = aluno.inep
        todos_alunos[aluno.email]['municipio'] = aluno.municipio
        todos_alunos[aluno.email]['cre'] = aluno.cre

    for professor in professores:
        todos_professores[professor.email] = {}
        todos_professores[professor.email]['email'] = professor.email
        todos_professores[professor.email]['inep'] = professor.inep
        todos_professores[professor.email]['municipio'] = professor.municipio
        todos_professores[professor.email]['cre'] = professor.cre



    ########################
    # CONSTRÓI OS INTERVALOS 
    ########################
    hoje = datetime.datetime.today()   
    intervalo_menor_sete_dias = {
        "inicio": datetime.date.today() - datetime.timedelta(days=7),
        "fim": datetime.date.today() - datetime.timedelta(days=1),
    }
    intervalo_maior_sete_menor_quartorze = {
        "inicio": datetime.date.today() - datetime.timedelta(days=15),
        "fim": datetime.date.today() - datetime.timedelta(days=8),
    }
    intervalo_maior_quatorze_menor_trinta = {
        "inicio": datetime.date.today() - datetime.timedelta(days=30),
        "fim": datetime.date.today() - datetime.timedelta(days=16),
    }
    intervalo_maior_trinta_menor_sessenta = {
        "inicio": datetime.date.today() - datetime.timedelta(days=60),
        "fim": datetime.date.today() - datetime.timedelta(days=31),
    }
    intervalo_maior_sessenta = {
        "ultimo": datetime.date.today() - datetime.timedelta(days=61),
    }
  
    intervalos = []
    intervalos.append((intervalo_menor_sete_dias))
    intervalos.append((intervalo_maior_sete_menor_quartorze))
    intervalos.append((intervalo_maior_quatorze_menor_trinta))
    intervalos.append((intervalo_maior_trinta_menor_sessenta))
    intervalos.append((intervalo_maior_sessenta))
    # print(intervalos)

    reports = []
    started = False
    labels =[]
    labels.append('menor_sete')
    labels.append('maior_sete_menor_quatorze')
    labels.append('maior_quatorze_menor_trinta')
    labels.append('maior_trinta_menor_sessenta')
    labels.append('maior_sessenta')


    ########################
    # PEGA OS DADOS DO GSUITE
    ########################
    i = 0
    trava = {} 
    agregacao = {}
    quants = {}
    for intervalo in intervalos: #por intervalo
        label = labels[i]
        grupo = labels[i]
        agregacao[label] = {}
        i += 1
        while True:
            inicio = ""
            fim = ""
            if 'ultimo' not in intervalo:
                inicio = "{}T00:00:00Z".format(intervalo['inicio'].strftime('%Y-%m-%d'))
                fim = "{}T23:59:00Z".format(intervalo['fim'].strftime('%Y-%m-%d'))
            else:
                inicio = "2020-06-01T00:00:00Z"
                fim = "{}T23:59:00Z".format(intervalo['ultimo'].strftime('%Y-%m-%d'))
 

            if not started:
                report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login',startTime=inicio,endTime=fim).execute()
                pageToken = report.get("nextPageToken")
                reports += report.get("items")
                started = True  
            else:
                report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login', maxResults=1000,startTime=inicio,endTime=fim,pageToken=pageToken).execute()
                pageToken = report.get("nextPageToken")
                reports += report.get("items")  

            if 'nextPageToken' not in report or 'items' not in report:
                break
        

        
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
            if identificacao_unica_usuario in todos_alunos:
                user = todos_alunos.get(identificacao_unica_usuario)
                role = 'Aluno'
            elif identificacao_unica_usuario in todos_professores:    
                user = todos_professores.get(identificacao_unica_usuario)
                role='Professor'
            else:
                continue
            
            # só processa se for aluno
            # agrega o as datas por email
            if user and role == 'Aluno' and user['email'] not in contabilizador and user['email'] not in trava:
                contabilizador[user['email']] = {
                        'inep':user['inep'],
                        'cre':user['cre'],
                        'municipio':user['municipio']
                    }
                trava[user['email']] = 'processado'
                
            
        ########################
        # CONTABILIZA OS DADOS POR INEP
        ########################
        for email in contabilizador:
            dados = contabilizador[email]
            if dados['inep'] not in quants:
                quants[dados['inep']] = {}
                quants[dados['inep']][label] = 0
                quants[dados['inep']]['cre'] = dados['cre']
                quants[dados['inep']]['municipio'] = dados['municipio']
                quants[dados['inep']][label] += 1
                quants[dados['inep']]['total'] = 0
                quants[dados['inep']]['total'] += 1
                

            else:
                if label not in quants[dados['inep']]:
                    quants[dados['inep']][label] = 0   
                quants[dados['inep']][label] += 1
                quants[dados['inep']]['total'] += 1


        started=False
        reports = []
        
    ########################
    # GRAVA TOTAL GERAL NO BANCO
    ########################
    for inep in quants:
        data = quants[inep]
        try:
            total_alunos_inep = alunos.filter(inep=inep)
            quants[inep]['total_geral'] = len(total_alunos_inep)
            
        except Exception as e:
            pass
    
    
    ########################
    # GRAVA NO BANCO DE DADOS
    ########################
    for inep in quants:
        data = quants[inep]
        try:
            escola = escolas.get(inep=inep)
            NovoDispersaoAluno.objects.create(
                data = datetime.date.today().strftime('%Y-%m-%d'),
                menor_sete = data.get('menor_sete',0),
                maior_sete_menor_quatorze = data.get('maior_sete_menor_quatorze',0),
                maior_quatorze_menor_trinta = data.get('maior_quatorze_menor_trinta',0),
                maior_trinta_menor_sessenta = data.get('maior_trinta_menor_sessenta',0),
                maior_sessenta = data.get('maior_sessenta',0),

                inep = inep ,
                cre = escola.cre ,
                municipio = data['municipio'] 
            )
        except Exception as e:
            print(e)
        
        try:            
            novo_ia =NovoIaAluno(
                data = datetime.date.today().strftime('%Y-%m-%d'),
                inep = inep ,
                cre = escola.cre ,
                municipio = data['municipio'] ,
                total_alunos = data['total_geral'],
                total_logaram = data['total']
            )
            novo_ia.save()
        except Exception as e:
            print(e)
        
        
        try:   
            status = NovoStatusAluno.objects.get_or_create(
                inep = inep ,
                cre = escola.cre ,
                municipio = data['municipio']
            )[0]
            status.total_alunos = data['total_geral']
            status.total_logaram = data['total']
            status.save()

        except Exception as e:
            print(e)
                        

        



    

    
