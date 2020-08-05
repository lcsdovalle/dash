from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco

ENV_DOMINIO = 'educar.rs.gov.br'
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly',
    ]
service_admin = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@{ENV_DOMINIO}"
    ).getService('admin','directory_v1')
service_class = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@{ENV_DOMINIO}"
    ).getService('classroom','v1')

db = banco('localhost','getedu','getedu00','dashboard_rs')

def carregar_professor(atv_criador):
    condicao = "id_gsuite = '{}' ".format(atv_criador)
    db.tabela('professores').ler(condicao)
    db.executar()
    prof = db.result.fetchall()
    prof_obj ={}
    if db.result.rowcount >0:
        prof_obj['email'] = prof[0][0]
        prof_obj['nome'] = prof[0][1]
        prof_obj['id'] = prof[0][8]
        return prof_obj
    else:
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
    condicao = "turma_id = '{}' ".format(atv_turma_id)
    db.tabela('turmas').ler(condicao)
    db.executar()
    turma = db.result.fetchall()
    turma_obj={}
    if db.result.rowcount >0:
        turma_obj['id'] = turma[0][0]
        turma_obj['escola_id'] = turma[0][2]
        turma_obj['escola_email'] = turma[0][3]
        return turma_obj
    else:
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
    condicao = "escola_email = '{}' ".format(escola_email)
    db.tabela('escolas').ler(condicao)
    db.executar()
    escola= db.result.fetchall()
    escola_obj={}
    if db.result.rowcount >0:
        escola_obj['escola_email'] = escola[0][0]
        escola_obj['escola_nome'] = escola[0][1]
        escola_obj['escola_inep'] = escola[0][2]
        escola_obj['escola_municipio'] = escola[0][3]
        escola_obj['escola_cre'] = escola[0][4]
        return escola_obj
    else:
        return False

if __name__ == "__main__":
    atividades = db.tabela('atividades').ler().executar()
    for atividade in atividades:
        atv_id = atividade[0]
        atv_criador = atividade[1]
        atv_turma_id = atividade[2]
        atv_criacao = atividade[3]
        atv_atualizacao = atividade[4]

        professor = carregar_professor(atv_criador)        
        if professor:
            turma = carregar_turma(atv_turma_id)
            if turma:
                escola = carregar_escola(turma.get('escola_email'))
                if escola:

                    params = {}

                    params['atividade_id'] = '{}'.format(atv_id)
                    params['atividade_criacao'] = '{}'.format(atv_criacao)
                    params['atividade_atualizacao'] = '{}'.format(atv_atualizacao)

                    params['atividade_escola'] = '{}'.format(escola.get('escola_email','Nome não identificado'))
                    params['atividade_escola_nome'] = '{}'.format(escola.get('escola_nome','Nome não identificado'))
                    params['atividade_inep'] = '{}'.format(escola.get('escola_inep','Nome não identificado'))
                    params['atividade_cre'] = '{}'.format(escola.get('escola_cre','Nome não identificado'))
                    params['atividade_municipio'] = '{}'.format(escola.get('escola_municipio','Município não identificado'))
                    
                    params['atividade_turma'] = '{}'.format(turma.get('id','Turma não identificada'))

                    params['atividade_professor_nome'] = '{}'.format(professor.get('nome','Nome não identificado'))
                    params['atividade_professor_email'] = '{}'.format(professor.get('email','Email não identificado'))
                    params['atividade_professor_id'] = '{}'.format(professor.get('id','Id não identificado'))
                    

                    db.tabela('grafico_principal').inserir(params).executar()

        

