#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime


# alunosensalados = AlunoEnsalado.objects.all()
# todosalunosensaladosporinep = {}
# for aensalado in alunosensalados:
#     if aensalado.inep not in todosalunosensaladosporinep:
#         todosalunosensaladosporinep[aensalado.inep] = 1
#     else:
#         todosalunosensaladosporinep[aensalado.inep] += 1 
# print("Alunos ensalados carregados na memória")


escopos = [
        # 'https://www.googleapis.com/auth/classroom.courses',
        # 'https://www.googleapis.com/auth/classroom.courses.readonly',
        # 'https://www.googleapis.com/auth/classroom.rosters',
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly', 
        'https://www.googleapis.com/auth/admin.reports.audit.readonly',
        # 'https://www.googleapis.com/auth/classroom.coursework.students',
        # 'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        # 'https://www.googleapis.com/auth/classroom.coursework.me',
        # 'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    ]
service_class = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@educar.rs.gov.br"
    ).getService('classroom','v1')
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
    hoje = datetime.datetime.today() - datetime.timedelta(days=1)
    # hoje = datetime.datetime.today()   - datetime.timedelta(days=1)
    intervalo_menor_sete_dias = {
        "inicio": hoje - datetime.timedelta(days=7),
        "fim": hoje,
        # "inicio": datetime.date.today() - datetime.timedelta(days=7),
        # "fim": datetime.date.today() - datetime.timedelta(days=1),
    }
    intervalo_maior_sete_menor_quartorze = {
        # "inicio": datetime.date.today() - datetime.timedelta(days=15),
        # "fim": datetime.date.today() - datetime.timedelta(days=8),
        "inicio": hoje - datetime.timedelta(days=15),
        "fim": hoje - datetime.timedelta(days=8),
    }
    intervalo_maior_quatorze_menor_trinta = {
        "inicio": hoje - datetime.timedelta(days=30),
        "fim": hoje - datetime.timedelta(days=16),
        # "inicio": datetime.date.today() - datetime.timedelta(days=30),
        # "fim": datetime.date.today() - datetime.timedelta(days=16),
    }
    intervalo_maior_trinta_menor_sessenta = {
        "inicio": hoje - datetime.timedelta(days=60),
        "fim": hoje - datetime.timedelta(days=31),
        # "inicio": datetime.date.today() - datetime.timedelta(days=60),
        # "fim": datetime.date.today() - datetime.timedelta(days=31),
    }
    intervalo_maior_sessenta = {
        # "ultimo": datetime.date.today() - datetime.timedelta(days=61),
        "ultimo": datetime.date.today() - datetime.timedelta(days=60),
    }
  
  
    intervalos = {}
    intervalos['menor_sete']                    = intervalo_menor_sete_dias
    intervalos['maior_sete_menor_quatorze'] = intervalo_maior_sete_menor_quartorze
    intervalos['maior_quatorze_menor_trinta'] = intervalo_maior_quatorze_menor_trinta
    intervalos['maior_trinta_menor_sessenta'] = intervalo_maior_trinta_menor_sessenta
    intervalos['maior_sessenta'] = intervalo_maior_sessenta

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
            adata_acesso = data_acesso_usuario.split('T')[0] # monta a data para comparação
            

            #verifica se é aluno ou professor
            if identificacao_unica_usuario in todos_alunos:
                user = todos_alunos.get(identificacao_unica_usuario)
                role = 'Aluno'
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
                quants[dados['inep']]['total_logaram'] = 0
                quants[dados['inep']]['total_logaram'] += 1
                quants[dados['inep']]['total_geral'] = todos_alunos_por_inep[dados['inep']]
                # quants[dados['inep']]['total_logaram'] = 1 if '1970' not in dados['ultimo_acesso'] else 0

                

            else:
                if label not in quants[dados['inep']]:
                    quants[dados['inep']][label] = 0   
                quants[dados['inep']][label] += 1
                quants[dados['inep']]['total_logaram'] += 1
                quants[dados['inep']]['total_geral'] = todos_alunos_por_inep[dados['inep']]
                # quants[dados['inep']]['total_logaram'] = 1 if '1970' not in dados['ultimo_acesso'] else 0


        started=False
        reports = []
        

    ########################
    # GRAVA NO BANCO DE DADOS
    ########################
    print("Agora vai gravar no banco")
    for inep in quants:
        data = quants[inep]
        cre = escolastodas[inep]["cre"]
        try:
            hoje = datetime.datetime.today()
            hoje = hoje.strftime('%Y-%m-%d')
            # escola = escolastodas.get(inep=inep)
            NovoDispersaoAluno.objects.create(
                data = hoje,
                menor_sete = data.get('menor_sete',0),
                maior_sete_menor_quatorze = data.get('maior_sete_menor_quatorze',0),
                maior_quatorze_menor_trinta = data.get('maior_quatorze_menor_trinta',0),
                maior_trinta_menor_sessenta = data.get('maior_trinta_menor_sessenta',0),
                maior_sessenta = data.get('maior_sessenta',0),

                inep = inep ,
                cre = cre ,
                municipio = data['municipio'] 
            )
        except Exception as e:
            print(e)
        
        try:            
            novo_ia =NovoIaAluno(
                data =hoje,
                inep = inep ,
                cre = cre ,
                municipio = data['municipio'] ,
                total_alunos = data['total_geral'],
                total_logaram = data['total_logaram']
            )
            novo_ia.save()
        except Exception as e:
            print(e)
        
        
        try:   
            status = NovoStatusAluno.objects.get_or_create(
                inep = inep ,
                cre = cre ,
                municipio = data['municipio']
            )[0]
            status.total_alunos = data['total_geral']
            status.total_logaram = data['total_logaram']
            status.save()

        except Exception as e:
            print(e)
