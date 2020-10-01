#pylint: disable=no-member

import os
import django
import signal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Atividade, NovoCadastroAtividades
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime
escopos = [
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.coursework.students',
        'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        'https://www.googleapis.com/auth/classroom.coursework.me',
        'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    ]
service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')
data_processamento = datetime.datetime.today().strftime('%Y-%m-%d')
def carregar_atividades(turma_id):
    aa = service_class.courses().courseWork().list(
        courseId=turma_id,
        pageSize=1,
        orderBy='updateTime desc'
    ).execute()
    
    pagetoken = aa.get('nextPageToken',False) 
    if pagetoken:
        todas_atividades = []
        while True:

            atividades = service_class.courses().courseWork().list(
                courseId=turma_id,
                pageSize=500,
                pageToken=pagetoken,
                orderBy='updateTime desc'
            ).execute()
            
            pagetoken = atividades.get('nextPageToken',False)



            if len(aa) == 1:
                todas_atividades = aa.get('courseWork') + atividades.get('courseWork')
                aa['courseWork'] = 0
            else:
                todas_atividades += atividades.get('courseWork')
            
            if 'nextPageToken' not in atividades or not pagetoken :
                retornar = []
                data_ref = datetime.datetime.now() - datetime.timedelta(days=30)
                
                for atv in todas_atividades:
                    data =  atv.get('creationTime').split('T')[0]
                    data = datetime.datetime.strptime(data,'%Y-%m-%d')

                    if data.timestamp() > data_ref.timestamp():
                        retornar.append(atv)

                return retornar
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
                        courseWorkId=atividade_id,
                        pageSize=500
                    ).execute()
                    alunos_atividade
                    
                    qtd_vinculos = 0
                    qtd_atrasos = 0
                    qtd_corrigida = 0
                    qtd_nao_iniciada = 0
                    qtd_iniciada = 0

                    if 'studentSubmissions' in alunos_atividade:
                        for atv in alunos_atividade.get('studentSubmissions'):
                           
                            qtd_nao_iniciada += 1 if 'NEW' in atv['state'] or 'CREATED' in atv['state'] else 0
                            qtd_atrasos += 1 if 'late' in atv else 0
                            qtd_corrigida += 1 if 'assignedGrade' in atv or 'RETURNED' == atv['state']  else 0
                            qtd_vinculos = len(alunos_atividade.get('studentSubmissions'))
                            qtd_iniciada += 1 if 'NEW' not in atv['state'] and 'CREATED' not in atv['state'] else 0
                        
                        novo = NovoCadastroAtividades(
                            data = data_processamento,
                            data_publicacao = a.get('creationTime').split('T')[0],
                            inep = t.inep,
                            
                            cre = t.cre,
                            municipio = t.municipio,
                            criador = a.get('creatorUserId'),
                            atividade_id = a.get('id'),
                            turma_id = t.turma_id,
                            qtd_iniciada =qtd_iniciada,
                            qtd_corrigida = qtd_corrigida,
                            qtd_nao_iniciada = qtd_nao_iniciada,
                            qtd_atrasos = qtd_atrasos,
                            qtd_vinculos = qtd_vinculos
                        )
                        novo
                        novo.save()
                except Exception as e:
                    print(e)
                    pass
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