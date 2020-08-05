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

db = banco('0.tcp.sa.ngrok.io','getedu','getedu00','dashboard_rs',porta=16152)
logger = PyCsv('logs/turmas')
def execute(t):    
    atividades = carregar_atividades(t)
    
    if atividades is not None:
        param = {}
        for a in atividades:
            try:
                param['atividade_id'] = '{}'.format(a.get('id'))
                param['turma_id'] = '{}'.format(a.get('courseId'))
                param['atividade_criacao'] = '{}'.format(a.get('creationTime'))
                param['atividade_atualizacao'] = '{}'.format(a.get('updateTime'))
                param['atividade_criador'] = '{}'.format(a.get('creatorUserId'))
                db.tabela('atividades').inserir(param).executar()
                # print(f"Atividade {a.get('id')} cadastrada com sucesso!")
            except Exception as e:
                print(f"Erro: {str(e)}")
if __name__ == "__main__":
    db.tabela('turmas').ler().executar()
    pool = Pool(20)
    # gravar = banco('localhost','getedu','getedu00','dashboard_rs')

    turmas = db.result.fetchall()
    proc = []
    for t in turmas:
        t
        proc.append(pool.apply_async(execute,(t[0],)))
    
    pool.close()
    pool.join()
