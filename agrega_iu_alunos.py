#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Atividade,IaIndicadorAluno, NovoIuAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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
    resultado = PyCsv("resultado")
    quantitativos = PyCsv("quantitativos")
    totais = PyCsv("totais")
    hoje = datetime.datetime.today()   
    intervalo = [
        datetime.date.today() - datetime.timedelta(days=7),
        datetime.date.today() - datetime.timedelta(days=6),
        datetime.date.today() - datetime.timedelta(days=5),
        datetime.date.today() - datetime.timedelta(days=4),
        datetime.date.today() - datetime.timedelta(days=3),
        datetime.date.today() - datetime.timedelta(days=2),
        datetime.date.today() - datetime.timedelta(days=1)
    ]
    intervalo = list(map(toStr,intervalo))     
    print(intervalo)
    alunos = Aluno.objects.all()
    professores = Professor.objects.all()
    todos_alunos = {}
    todos_professores = {}
    for aluno in alunos:
        todos_alunos[aluno.email] = {}
        todos_alunos[aluno.email]['email'] = aluno.email
        todos_alunos[aluno.email]['inep'] = aluno.inep

    # for professor in professores:
    #     todos_professores[professor.email] = {}
    #     todos_professores[professor.email]['email'] = professor.email
    #     todos_professores[professor.email]['inep'] = professor.inep

    sete_dias = datetime.datetime.today() - datetime.timedelta(days=7)

    domingo = datetime.datetime.today() 
    domingo = "{}T23:59:00Z".format(domingo.strftime('%Y-%m-%d'))
    sete_dias = "{}T00:00:00Z".format(sete_dias.strftime('%Y-%m-%d'))
    reports = []
    started = False
    pageToken=True
    print(sete_dias)
    print(domingo)
    print(datetime.date.today())
    while pageToken is not None:
        if not started:
            try:
                report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login',startTime=sete_dias,endTime=domingo).execute()
                pageToken = report.get("nextPageToken",None)
                reports += report.get("items")
                started = True
            except Exception as e:
                continue  
        else:
            try:
                report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk71mbipbf',applicationName='login', maxResults=1000,startTime=sete_dias,endTime=domingo,pageToken=pageToken).execute()
                pageToken = report.get("nextPageToken",None)
                reports += report.get("items")  
            except Exception as e:
                continue  

            

  
    
    
    reports
    contabilizador = {}    

    for r in reports:
        user = False
        identificacao_unica_usuario = r.get('actor').get('email') #pega o email
        data_acesso_usuario = r.get('id').get('time') # pega o time
        adata_acesso = data_acesso_usuario.split('T')[0]
        
        if identificacao_unica_usuario in todos_alunos:
            user = todos_alunos.get(identificacao_unica_usuario)
            role = 'Aluno'

        else:
            continue

        if user and role == 'Aluno':

            if user['email'] not in contabilizador:            
                contabilizador[user['email']] = {}
                contabilizador[user['email']]['dias'] = []
                contabilizador[user['email']]['inep'] = user['inep']

    
            if adata_acesso not in contabilizador[user['email']]['dias'] and adata_acesso in intervalo:
                contabilizador[user['email']]['dias'].append(str(adata_acesso))



    ineps = {}
    quants = {}
    for email in contabilizador:
        usuario = contabilizador[email]
        
        if usuario['inep'] not in ineps:
            ineps[usuario['inep']] = {}
            ineps[usuario['inep']]['a_um_dia'] = 1 if len(usuario['dias']) == 1 else 0
            ineps[usuario['inep']]['a_dois_dia'] = 1 if len(usuario['dias']) == 2 else 0
            ineps[usuario['inep']]['a_tres_dia'] = 1 if len(usuario['dias']) == 3 else 0
            ineps[usuario['inep']]['a_quatro_dia'] = 1 if len(usuario['dias']) == 4 else 0
            ineps[usuario['inep']]['a_cinco_dia'] = 1 if len(usuario['dias']) == 5 else 0
            ineps[usuario['inep']]['a_seis_dia'] = 1 if len(usuario['dias']) == 6 else 0
            ineps[usuario['inep']]['a_sete_dia'] = 1 if len(usuario['dias']) == 7 else 0
            ineps[usuario['inep']]['a_nenhum_dia'] = 1 if len(usuario['dias']) == 0 else 0
        else:
            ineps[usuario['inep']]['a_um_dia'] += 1 if len(usuario['dias']) == 1 else 0
            ineps[usuario['inep']]['a_dois_dia'] += 1 if len(usuario['dias']) == 2 else 0
            ineps[usuario['inep']]['a_tres_dia'] += 1 if len(usuario['dias']) == 3 else 0
            ineps[usuario['inep']]['a_quatro_dia'] += 1 if len(usuario['dias']) == 4 else 0
            ineps[usuario['inep']]['a_cinco_dia'] += 1 if len(usuario['dias']) == 5 else 0
            ineps[usuario['inep']]['a_seis_dia'] += 1 if len(usuario['dias']) == 6 else 0
            ineps[usuario['inep']]['a_sete_dia'] += 1 if len(usuario['dias']) == 7 else 0
            ineps[usuario['inep']]['a_nenhum_dia'] += 1 if len(usuario['dias']) == 0 else 0
   
   
    escolas = Escola.objects.all()
    for inep in ineps:
        item = ineps[inep]
        try:
            escola = escolas.get(inep=inep)
            iu =  NovoIuAluno(
                data = datetime.date.today().strftime('%Y-%m-%d'),
                inep = inep,
                escola = escola.nome,
                municipio = escola.municipio,
                cre = escola.cre,
                a_um_dia = item.get('a_um_dia',0),
                a_dois_dias = item.get('a_dois_dia',0),
                a_tres_dias = item.get('a_tres_dia',0),
                a_quatro_dias = item.get('a_quatro_dia',0),
                a_cinco_dias = item.get('a_cinco_dia',0),
                a_seis_dias = item.get('a_seis_dia',0),
                a_sete_dias = item.get('a_sete_dia',0),
                a_nenhum_dia = item.get('a_nenhum_dia',0)
            )
            iu
            iu.save()
        except Exception as e:
            print(e)
        # quants[email] = len(usuario['dias'])

        # for dia in usuario['dias']:
        #     resultado.add_row_csv([
        #         email,
        #         dia,
        #         ])     
    # um = 0
    # dois = 0
    # tres = 0
    # quatro = 0
    # cinco = 0
    # seis = 0
    # sete = 0
    # for item in quants:
    #     itemr = quants[item]
    #     um += 1 if itemr == 1 else 0
    #     dois += 1 if itemr == 2 else 0
    #     tres += 1 if itemr == 3 else 0
    #     quatro += 1 if itemr == 4 else 0
    #     cinco += 1 if itemr == 5 else 0
    #     seis += 1 if itemr == 6 else 0
    #     sete += 1 if itemr == 7 else 0
    

    
    # totais.add_row_csv([
    #     'um','dois','tres','quatro','cinco','seis','sete'
    # ])
    # totais.add_row_csv([
    #   um,dois,tres,quatro,cinco,seis,sete
    # ])
                
    # desconto = datetime.timedelta(days=1)

    # data_corrente = datetime.date.today() - desconto
    # data_corrente = data_corrente.strftime('%Y-%m-%d')    



     



    

    
