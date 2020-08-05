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
        # 'https://www.googleapis.com/auth/classroom.coursework.students',
        # 'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        # 'https://www.googleapis.com/auth/classroom.coursework.me',
        # 'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    ]
service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')



class Escola():
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



db = banco('localhost','getedu','getedu00','dashboard_rs')
logger = PyCsv('logs/turmas')
def execute(e):    
    AEscola = Escola(str(e))
    AEscola.carregar_turmas()
    param = {}
    if len(AEscola.turmas) >0:

        for turma in AEscola.turmas:
            name = removeBarraN().get(turma.get('name'))
            param['turma_id'] = int(turma.get('id'))
            # param['turma_title'] = '{}'.format(name)
            param['turma_criador'] = '{}'.format(turma.get('ownerId'))
            param['turma_criador_email'] = '{}'.format(e)
            try:
                db.tabela('turmas').inserir(param).executar()                                
            except Exception as e:
                print(f"Falhou {str(e)}")
if __name__ == "__main__":
    db.tabela('escolas').ler().executar()
    pool = Pool(20)
    # gravar = banco('localhost','getedu','getedu00','dashboard_rs')

    escolas = db.result.fetchall()
    proc = []
    for e in escolas:
        e = e[0].replace(' ','')
        proc.append(pool.apply_async(execute,(e,)))
    
    pool.close()
    pool.join()
