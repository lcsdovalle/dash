#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import Turmas,NovoDispersaoProfessor,FuncaoDocente, Meet,Atividade, NovoIaPRofessor, NovoStatusProfessor, NovoIuProfessor, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime


csv = PyCsv("meets_por_inep_por_alunos")
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly', 
        'https://www.googleapis.com/auth/admin.reports.audit.readonly',
    ]
a_lista = PyCsv('nova-consolidacao-por-professores')
#service_class = authService( escopos,'jsons/cred_rs2.json',f"getedu@educar.rs.gov.br").getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    # MONTA OS CSVS
    resultado = PyCsv("resultado")
    quantitativos = PyCsv("quantitativos")
    totais = PyCsv("totais")

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    professores = Professor.objects.all()
    todos_professores = {}
    for professor in professores:
        todos_professores[professor.email] = {}
        todos_professores[professor.email]['email'] = professor.email
        todos_professores[professor.email]['inep'] = professor.inep
        todos_professores[professor.email]['municipio'] = professor.municipio
        todos_professores[professor.email]['cre'] = professor.cre
        todos_professores[professor.email]['id'] = professor.professor_id
        todos_professores[professor.email]['nome'] = professor.nome
    
    alunos = Aluno.objects.all()
    todos_alunos = {}

    for aluno in alunos:
        todos_alunos[aluno.email] = {}
        todos_alunos[aluno.email]['email'] = aluno.email
        todos_alunos[aluno.email]['inep'] = aluno.inep
        todos_alunos[aluno.email]['municipio'] = aluno.municipio
        todos_alunos[aluno.email]['cre'] = aluno.cre
        
    # PEGA OS DADOS DO GSUITE
    ########################
    trava = {} 
    quants = {}

    for email in todos_professores: #percorre cada professor do banco
        pageToken = True
        started = False
        professor = todos_professores[email]
        reports = []
        while pageToken is not None: # carrega todos os eventos do meet os quais o professor foi organizador
            if not started:
                try:
                    report = report_service.activities().list(userKey='all',filters=f"organizer_email=={email}", applicationName='meet').execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")
                
                    started = True 
                except Exception as e:
                    print(e)
                    continue 
            else:
                try:
                    report = report_service.activities().list(userKey='all',applicationName='meet',filters=f"organizer_email=={email}", maxResults=1000,pageToken=pageToken).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")  
                    
                except Exception as e:
                    continue 
        actores = {}
        por_meet = {}
        reports
        inep = False
        for item in reports:
            eventos = item.get('events') # carrega os eventos
            try: # verifica se é aluno
                participante =item.get('actor').get('email')
                aluno = todos_alunos[participante]
                inep = todos_alunos[participante]['inep'] # se for aluno captura o inep para identificação do meet
                print("É aluno")
            except Exception as e:
                print("Não é aluno")

            if inep: # se foi aluno e possui inep, então procede
                for evento in eventos:
                    parameters = evento.get('parameters')
                    
                    duracao = 0
                    for param in parameters:
                        if param.get('name') == 'duration_seconds':
                            duracao += int(param.get('value',0))

                        if param.get('name') == 'meeting_code': #verifica se o parâmetro é o codigo do meet
                            if param['value'] not in por_meet: # se for coloca ele na memória para agregações
                                por_meet[param['value']] = {}
                                por_meet[param['value']]['inep'] = inep
                                por_meet[param['value']]['participantes'] = 0
                                por_meet[param['value']]['time'] =item.get('id').get('time').split('T')[0]

                                if duracao !=0:
                                    por_meet[param['value']]['duracao'] = duracao or 0  
                                
                            if param['value'] in por_meet: # verifica se o meet já foi adicionado a memória
                                por_meet[param['value']]['participantes'] += 1 # se já, então contabiliza um participante
                            
        if len(por_meet) >0:
            for code in por_meet:
                meet = por_meet[code]
                csv.add_row_csv([
                    professor['email'],
                    professor['nome'],
                    professor['id'],
                    code,
                    meet['inep'],
                    meet['participantes'],
                    meet['time'],
                    meet.get('duracao',0)
                ])
                        
        

           