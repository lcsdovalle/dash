import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from engajamento.models import Professor,Aluno,Atividade,Escola,Turmas,GraficoGeral
from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco

ENV_DOMINIO = 'sed.sc.gov.br'
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly',
    ]
service_admin = authService(
    escopos,
    'jsons/cred_sc.json',
    f"gam@{ENV_DOMINIO}"
    ).getService('admin','directory_v1')
service_class = authService(
    escopos,
    'jsons/cred_sc.json',
    f"gam@{ENV_DOMINIO}"
    ).getService('classroom','v1')



def carregar_professor(atv_criador):
    
    try:
        prof = Professor.objects.get(professor_id__exact=atv_criador)    
        prof_obj ={}
        
        prof_obj['email'] = prof.email
        prof_obj['nome'] = prof.nome
        prof_obj['id'] = prof.id
        return prof_obj
    except:
        try:
            prof = service_admin.users().get(userKey=atv_criador).execute()
            if 'primaryEmail' in prof:                
                prof_obj['nome'] = prof.get('name').get('fullName')
                prof_obj['email'] = prof.get('primaryEmail')
                prof_obj['id'] = prof.get('id')                
                return prof_obj
            else:
                return False

        except Exception as e:
            return False
def obter_email_escola_no_gsuite(escola_id):
        try:
            escola = service_admin.users().get(userKey=escola_id).execute()
            return escola.get('primaryEmail')
        except Exception as e:
            print(e)
            return False
def carregar_turma(atv_turma_id):
    try:
        turma = Turmas.objects.get(turma_id__exact=atv_turma_id)
        
        turma_obj={}
        
        if turma is not None :        
            turma_obj['id'] = turma.turma_id
            turma_obj['escola_id'] = turma.owner_id
            turma_obj['escola_email'] = turma.owner_email
            return turma_obj
    except:
        try:
            turma = service_class.courses().get(id=atv_turma_id).execute()
            if 'id' in turma:
                turma_obj['id'] = turma.get('id') 
                turma_obj['escola_id'] = turma.get('ownerId') 
                turma_obj['escola_email'] = (
                        obter_email_escola_no_gsuite(turma_obj['escola_id']) 
                    )
                return turma_obj
            else:
                return False

        except Exception as e:
            return False

def carregar_escola(escola_email):
    try:
        escola = Escola.objects.get(email=escola_email)
        escola_obj={}    
        escola_obj['escola_email'] = escola.email
        escola_obj['escola_nome'] = escola.nome
        escola_obj['escola_inep'] = escola.inep
        escola_obj['escola_municipio'] = escola.municipio
        escola_obj['escola_cre'] = escola.cre
        escola_obj['escola_regiao'] = escola.regiao
        return escola_obj
    except:    
        return False

if __name__ == "__main__":
    # atividades = db.tabela('atividades').ler().executar()
    atividades = Atividade.objects.all()

    for atividade in atividades:
        atv_id = atividade.atividade_id
        atv_criador = atividade.creator_id
        atv_turma_id = atividade.turma_id
        atv_criacao = atividade.criado
        atv_atualizacao = atividade.atualizado

        professor = carregar_professor(atv_criador)        
        if professor:
            turma = carregar_turma(atv_turma_id)
            if turma:
                escola = carregar_escola(turma.get('escola_email'))
                if escola:

                    atv = GraficoGeral.objects.create(

                        atividade_id            = atv_id,
                        atividade_criacao       = atv_criacao,
                        atividade_atualizacao   = atv_atualizacao,

                        escola_email            = escola.get('escola_email','Não detectado'),
                        escola_nome             = escola.get('escola_nome','Não detectado'),
                        escola_inep             = escola.get('inep','000000'),

                        municipio               = escola.get('escola_municipio'),
                        regiao                  = escola.get('escola_regiao'),

                        professor_nome          = professor.get('nome'),
                        professor_email         = professor.get('email'),
                        professor_id            = professor.get('id')
                    )                

                    print(atv)