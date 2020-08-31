import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Escola
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
escopos = [
        'https://www.googleapis.com/auth/classroom.courses',
    ]
service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')



class Escolas():
    def __init__(self,escola_email):
        self.escola_email= escola_email
        self.erro = False
        self.turmas = []
        self.entregas = []
    def carregar_turmas(self):
        try:
            todas_turmas = []
            primeira_turma = service_class.courses().list(teacherId=self.escola_email,pageSize=1).execute()
            pagetoken = primeira_turma.get('nextPageToken')
            
            while True:
                demais_turmas = service_class.courses().list(teacherId=self.escola_email,pageToken=pagetoken,pageSize=500).execute()
                
                pagetoken = demais_turmas.get("nextPageToken",False)

                todas_turmas = ( primeira_turma.get('courses',[]) + demais_turmas.get('courses',[])
                    if len(primeira_turma.get('courses',[]) ) == 1 and len(demais_turmas.get("courses",[])) > 1 else
                    demais_turmas.get('courses',[])
                )

                self.turmas +=todas_turmas

                if 'nextPageToken' not in demais_turmas or len(demais_turmas.get('courses')) < 500 or not pagetoken:
                    return self.turmas            

        except Exception as e:
            self.erro =e
    def contabilizar_entregas(self,turma_id,atividade_id):
        todos_alunos = False
        primeiro_aluno = service_class.courses().courseWork().studentSubmissions().list(
            courseId= turma_id,
            courseWorkId = atividade_id,
            pageSize=1
        ).execute()
        
        pagetoken = primeiro_aluno.get('nextPageToken')

        while True:
            demais_aluno = service_class.courses().courseWork().studentSubmissions().list(
                courseId= turma_id,
                courseWorkId = atividade_id,
                pageSize=30,
                pageToken=pagetoken
            ).execute()
            
            pagetoken = demais_aluno.get('nextPageToken',False)

            todos_alunos = (
                primeiro_aluno.get('studentSubmissions',[]) + demais_aluno.get("studentSubmissions",[])
                if len(primeiro_aluno) ==1 else
                demais_aluno.get("studentSubmissions",False)
            )
            self.entregas += todos_alunos
            if 'nextPageToken' not in demais_aluno or len(demais_aluno) <30:
                return self.entregas
    def carregar_atividades(self,turma_id):
        try:
            atividades = service_class.courses().courseWork().list(
                courseId=turma_id
            ).execute()
            
            if 'courseWork' in atividades and atividades.get('courseWork',False):
                return atividades.get('courseWork')
            else:
                self.erro = "Turma sem atividades"                
        except Exception as e:
            self.erro = e


def execute(e):        
    e
    AEscola = Escolas(str(e.email))
    AEscola.carregar_turmas()
    param = {}
    if len(AEscola.turmas) >0:

        for turma in AEscola.turmas:
            try:                
                t = Turmas.objects.create(
                    turma_id=turma.get('id'),
                    owner_id=turma.get('ownerId'),                    
                    owner_email=e.email,
                    inep=e.inep,
                    municipio=e.municipio,
                    cre=e.cre
                )
                # print(t)
            except Exception as err:
                print(f"Falhou {str(err)}")
if __name__ == "__main__":
    pool = Pool(1)
    # gravar = banco('localhost','getedu','getedu00','dashboard_rs')

    escolas = Escola.objects.all()
    proc = []
    for e in escolas:        
        proc.append(pool.apply_async(execute,(e,)))
    
    pool.close()
    pool.join()