#pylint: disable=no-member

import os
import django
import signal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Atividade
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
escopos = [
        'https://www.googleapis.com/auth/classroom.courses',
        # 'https://www.googleapis.com/auth/classroom.courses.readonly',
        # 'https://www.googleapis.com/auth/classroom.rosters',
        # 'https://www.googleapis.com/auth/classroom.profile.emails',
        # 'https://www.googleapis.com/auth/classroom.profile.photos',
        'https://www.googleapis.com/auth/classroom.coursework.students',
        'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        'https://www.googleapis.com/auth/classroom.coursework.me',
        'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    ]
service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')

def carregar_atividades(turma_id):
    aa = service_class.courses().courseWork().list(
        courseId=turma_id,
        pageSize=1
    ).execute()
    
    pagetoken = aa.get('nextPageToken',False) 
    if pagetoken:
        todas_atividades = []
        while True:

            atividades = service_class.courses().courseWork().list(
                courseId=turma_id,
                pageSize=500,
                pageToken=pagetoken
            ).execute()
            
            pagetoken = atividades.get('nextPageToken',False)

            if len(aa) == 1:
                todas_atividades = aa.get('courseWokr') + atividades.get('courseWork')
                aa['courseWork'] = 0
            else:
                todas_atividades += atividades.get('courseWork')
            
            if 'nextPageToken' not in atividades or not pagetoken or len(atividades) <500:
                return todas_atividades
                break

def execute(t):
    atividades = carregar_atividades(t.turma_id)    
    if atividades is not None:
        param = {}
        for a in atividades:
            try:
                atividade_id = a.get('id')
                turma_id = a.get('courseId')
                try:
                    alunos_atividade = service_class.courses().courseWork().studentSubmissions().list(
                        courseId=turma_id,
                        courseWorkId=atividade_id
                    ).execute()
                    alunos_atividade

                    

                except Exception as e:
                    print(e)
                    pass


                a = Atividade.objects.create(
                    # title = a.get('title'),
                    atividade_id = a.get('id'),
                    state = a.get('state'),
                    creator_id = a.get('creatorUserId'),
                    criado = a.get('creationTime'),
                    atualizado = a.get('updateTime'),
                    turma_id = a.get('courseId'),
                    inep=t.inep,
                    municipio=t.municipio,
                    cre=t.cre
                )
                print(a)                
            except Exception as e:
                print(f"Erro: {str(e)}")

def init_worker():
  signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == "__main__":
    
    pool = Pool(1, init_worker)    
    
    try:
        turmas = Turmas.objects.all()
        turmas
        proc = []
        for t in turmas:  
            t      
            proc.append(pool.apply_async(execute,(t,)))
        pool.close()
    except KeyboardInterrupt:
        pool.terminate()
    pool.join()