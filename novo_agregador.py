#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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
    
    hoje = datetime.datetime.today()   
    intervalo = [
        datetime.date.today() - datetime.timedelta(days=6),
        datetime.date.today() - datetime.timedelta(days=5),
        datetime.date.today() - datetime.timedelta(days=4),
        datetime.date.today() - datetime.timedelta(days=3),
        datetime.date.today() - datetime.timedelta(days=2),
        datetime.date.today() - datetime.timedelta(days=1),
        datetime.date.today(),
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

    for professor in professores:
        todos_professores[professor.email] = {}
        todos_professores[professor.email]['email'] = professor.email
        todos_professores[professor.email]['inep'] = professor.inep

    sete_dias = datetime.datetime.today() - datetime.timedelta(days=6)

    domingo = datetime.datetime.today()
    domingo = "{}T23:59:00Z".format(domingo.strftime('%Y-%m-%d'))
    sete_dias = "{}T00:00:00Z".format(sete_dias.strftime('%Y-%m-%d'))
    reports = []
    started = False
    print(sete_dias)
    print(domingo)
    print(datetime.date.today())
    while True:
        if not started:
            report = report_service.activities().list(userKey='all',applicationName='login',startTime=sete_dias).execute()
            pageToken = report.get("nextPageToken")
            reports += report.get("items")
            started = True  
        else:
            report = report_service.activities().list(userKey='all',applicationName='login', maxResults=1000,startTime=sete_dias,pageToken=pageToken).execute()
            pageToken = report.get("nextPageToken")
            reports += report.get("items")  
        if len(report['items']) < 1000 or 'nextPageToken' not in report or 'items' not in report:
            break
    
    
    
    reports
    contabilizador = {}    
   
    for r in reports:
        user = False
        identificacao_unica_usuario = r.get('actor').get('email') #pega o email
        data_acesso_usuario = r.get('id').get('time') # pega o time
        role = 'Aluno'

        if identificacao_unica_usuario in todos_alunos:
            user = todos_alunos.get(identificacao_unica_usuario)
        elif identificacao_unica_usuario in todos_professores:    
            user = todos_professores.get(identificacao_unica_usuario)
            role='Professor'
        else:
            continue
            
        if user:
            
            for dia in intervalo:

                if user['email'] not in contabilizador:            
                    contabilizador[user['email']] = {}
                    contabilizador[user['email']]['total_acessos'] = 0
                    contabilizador[user['email']]['dias'] = []

                    if str(dia) in data_acesso_usuario:
                    
                        if str(dia) not in contabilizador[user['email']]['dias']: 
                            contabilizador[user['email']]['total_acessos'] += 1 if str(dia) in data_acesso_usuario else 0
                            contabilizador[user['email']]['dias'].append(str(dia))

                    contabilizador[user['email']]['inep'] = user['inep']
                    contabilizador[user['email']]['papel'] = role

                else:
                    contabilizador[user['email']]['papel'] = role
                    if str(dia) in data_acesso_usuario:
                    
                        if str(dia) not in contabilizador[user['email']]['dias']: 
                            contabilizador[user['email']]['total_acessos'] += 1 if str(dia) in data_acesso_usuario else 0
                            contabilizador[user['email']]['dias'].append(str(dia))

    ineps = {}
    for linha in contabilizador:
        indicador = contabilizador[linha]
        for inep in indicador['inep'].split(","):
            if inep not in ineps:
                ineps[inep] = {}
                ineps[inep]['p_um_dia'] = 0
                ineps[inep]['p_dois_dias'] = 0
                ineps[inep]['p_tres_dias'] = 0
                ineps[inep]['p_quatro_dias'] = 0
                ineps[inep]['p_cinco_dias'] = 0
                ineps[inep]['p_seis_dias'] = 0
                ineps[inep]['p_sete_dias'] = 0
                ineps[inep]['p_nenhum_dia'] = 0

                ineps[inep]['a_um_dia'] = 0
                ineps[inep]['a_dois_dias'] = 0
                ineps[inep]['a_tres_dias'] = 0
                ineps[inep]['a_quatro_dias'] = 0
                ineps[inep]['a_cinco_dias'] = 0
                ineps[inep]['a_seis_dias'] = 0
                ineps[inep]['a_sete_dias'] = 0
                ineps[inep]['a_nenhum_dia'] = 0
            else:
                ineps[inep]['p_um_dia'] += 1 if indicador['total_acessos'] == 1 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_dois_dias'] += 1 if indicador['total_acessos'] == 2 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_tres_dias'] += 1 if indicador['total_acessos'] == 3 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_quatro_dias'] += 1 if indicador['total_acessos'] == 4 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_cinco_dias'] += 1 if indicador['total_acessos'] == 5 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_seis_dias'] += 1 if indicador['total_acessos'] == 6 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_sete_dias'] += 1 if indicador['total_acessos'] == 7 and 'Professor' ==  indicador['papel'].title()  else 0         
                ineps[inep]['p_nenhum_dia'] += 1 if indicador['total_acessos'] == 0 and 'Professor' ==  indicador['papel'].title()  else 0         
                
                ineps[inep]['a_um_dia'] += 1 if indicador['total_acessos'] == 1 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_dois_dias'] += 1 if indicador['total_acessos'] == 2 and 'Aluno' ==  indicador['papel'].title()  else 0
                ineps[inep]['a_tres_dias'] += 1 if indicador['total_acessos'] == 3 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_quatro_dias'] += 1 if indicador['total_acessos'] == 4 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_cinco_dias'] += 1 if indicador['total_acessos'] == 5 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_seis_dias'] += 1 if indicador['total_acessos'] == 6 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_sete_dias'] += 1 if indicador['total_acessos'] == 7 and 'Aluno' ==  indicador['papel'].title()  else 0         
                ineps[inep]['a_nenhum_dia'] += 1 if indicador['total_acessos'] == 0 and 'Aluno' ==  indicador['papel'].title()  else 0           

    desconto = datetime.timedelta(days=1)

    data_corrente = datetime.date.today() - desconto
    data_corrente = data_corrente.strftime('%Y-%m-%d')    
    try:
        for inep in ineps:
            try:
                escola = Escola.objects.get(inep=inep)
                total_alunos = ineps[inep]['a_um_dia'] + ineps[inep]['a_dois_dias'] + ineps[inep]['a_tres_dias'] + ineps[inep]['a_quatro_dias'] + ineps[inep]['a_cinco_dias'] + ineps[inep]['a_seis_dias'] + ineps[inep]['a_sete_dias'] 
                total_professores = ineps[inep]['p_um_dia'] + ineps[inep]['p_dois_dias'] + ineps[inep]['p_tres_dias'] + ineps[inep]['p_quatro_dias'] + ineps[inep]['p_cinco_dias'] + ineps[inep]['a_seis_dias'] + ineps[inep]['a_sete_dias']

                IndicadorDeFinalDeSemana.objects.create(
                    inep            = inep,
                    escola          = escola.nome,
                    cre             = escola.cre,
                    municipio       = escola.municipio,

                    data            = data_corrente,    

                    p_um_dia        = ineps[inep]['p_um_dia'],
                    p_dois_dias     = ineps[inep]['p_dois_dias'],
                    p_tres_dias     = ineps[inep]['p_tres_dias'],
                    p_quatro_dias   = ineps[inep]['p_quatro_dias'],
                    p_cinco_dias    = ineps[inep]['p_cinco_dias'],
                    p_seis_dias     = ineps[inep]['p_seis_dias'],
                    p_sete_dias     = ineps[inep]['p_sete_dias'],
                    p_nenhum_dia    = ineps[inep]['p_nenhum_dia'],
                    
                    a_um_dia        = ineps[inep]['a_um_dia'],
                    a_dois_dias     = ineps[inep]['a_dois_dias'],
                    a_tres_dias     = ineps[inep]['a_tres_dias'],
                    a_quatro_dias   = ineps[inep]['a_quatro_dias'],
                    a_cinco_dias    = ineps[inep]['a_cinco_dias'],
                    a_seis_dias     = ineps[inep]['a_seis_dias'],
                    a_sete_dias     = ineps[inep]['a_sete_dias'],
                    a_nenhum_dia    = ineps[inep]['a_nenhum_dia'],   

                    iu_aluno = ( (  ( ineps[inep]['a_tres_dias'] + ineps[inep]['a_quatro_dias'] + ineps[inep]['a_cinco_dias'] + ineps[inep]['a_seis_dias'] + ineps[inep]['a_sete_dias'] ) / total_alunos )  *100 ) if total_alunos > 0 else 0,
                    iu_professor = ( (  (ineps[inep]['p_tres_dias'] + ineps[inep]['p_quatro_dias'] + ineps[inep]['p_cinco_dias'] + ineps[inep]['p_seis_dias'] + ineps[inep]['p_sete_dias'] ) / total_professores ) *100  ) if total_professores > 0 else 0

                )

            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


     



    

    
