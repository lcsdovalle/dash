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

    atividades = Atividade.objects.all()
    todas_atividades_por_professor = {}
    for atv in atividades:
        if atv.creator_id not in todas_atividades_por_professor:
            todas_atividades_por_professor[atv.creator_id] =[]
            todas_atividades_por_professor[atv.creator_id].append(atv.criado)
        else:
            todas_atividades_por_professor[atv.creator_id].append(atv.criado)



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
        
    
    hoje = datetime.datetime.today()   
    intervaloss = [
        datetime.date.today() - datetime.timedelta(days=7),
        datetime.date.today() - datetime.timedelta(days=6),
        datetime.date.today() - datetime.timedelta(days=5),
        datetime.date.today() - datetime.timedelta(days=4),
        datetime.date.today() - datetime.timedelta(days=3),
        datetime.date.today() - datetime.timedelta(days=2),
        datetime.date.today() - datetime.timedelta(days=1)
    ]
    intervaloss = list(map(toStr,intervaloss))     
    ########################
    # CONSTRÓI OS INTERVALOS 
    ########################
    hoje = datetime.datetime.today()   

    
    intervalo_maior_trinta_menor_sessenta = {
        "inicio": datetime.date.today() - datetime.timedelta(days=60),
        "fim": datetime.date.today() - datetime.timedelta(days=1),
    }
    
    intervalos = {}
    intervalos['maior_trinta_menor_sessenta'] = intervalo_maior_trinta_menor_sessenta
    reports = []
 

    ########################
    # PEGA OS DADOS DO GSUITE
    ########################
    trava = {} 
    quants = {}


    for label in intervalos: #por intervalo
        pageToken = True
        intervalo = intervalos[label]
        started = False
        while pageToken is not None:
            inicio = ""
            fim = ""
            if 'ultimo' not in intervalo:
                inicio = "{}T00:00:00Z".format(intervalo['inicio'].strftime('%Y-%m-%d'))
                fim = "{}T23:59:00Z".format(intervalo['fim'].strftime('%Y-%m-%d'))
            else:
                inicio = "2020-06-01T00:00:00Z"
                fim = "{}T23:59:00Z".format(intervalo['ultimo'].strftime('%Y-%m-%d'))
 
            if not started:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk73768f3m',applicationName='login',endTime=fim).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")
                    started = True 
                except Exception as e:
                    continue 
            else:
                try:
                    report = report_service.activities().list(userKey='all',orgUnitID='id:02zfhnk73768f3m',applicationName='login', maxResults=1000,endTime=fim,pageToken=pageToken).execute()
                    pageToken = report.get("nextPageToken",None)
                    reports += report.get("items")  
                except Exception as e:
                    continue 
        

        ########################
        # CONTABILIZA OS DADOS POR USUÁRIOS
        ########################
        reports
        contabilizador = {}  
        for r in reports:
            user = False
            identificacao_unica_usuario = r.get('actor').get('email') #pega o email
            data_acesso_usuario = r.get('id').get('time') # pega o time
            adata_acesso = data_acesso_usuario.split('T')[0] # monta a data para comparação

            #verifica se é aluno ou professor
            if identificacao_unica_usuario in todos_professores:    
                user = todos_professores.get(identificacao_unica_usuario)
                role='Professor'
            else:
                continue

            if user['email'] not in contabilizador:            
                contabilizador[user['email']] = {}
                contabilizador[user['email']] = {
                        'inep':user['inep'],
                        'cre':user['cre'],
                        'municipio':user['municipio'],
                        'dias':[],
                        'id':user['id'],
                        'nome':user['nome']
                    }
            if adata_acesso not in contabilizador[user['email']]['dias']:
                contabilizador[user['email']]['dias'].append(str(adata_acesso))
        
    ineps = {}
    quants = {}
    for email in contabilizador:
        acessou_ultima_semana = 0
        usuario = contabilizador[email]





        os_dias = usuario.get('dias',False)
        os_dias.sort()
        if os_dias:
            total_acessos_desde_primeiro_login = len(usuario.get('dias',0))

            for dia in usuario.get('dias'): #percorre cada dia
                if dia in intervaloss: # verifica se o dia está no intervalo
                    acessou_ultima_semana +=1
            for inep in usuario.get('inep').split(','):
                try:
                    # atividades = Atividade.objects.filter(creator_id=usuario.get('id'))
                    atividades = todas_atividades_por_professor[usuario.get('id')]
                    total_atividades = len(atividades)
                    atv_ultimos_sete_dias = 0
                    for data in atividades:
                        if data.split("T")[0] in intervaloss:
                            atv_ultimos_sete_dias += 1


                except Exception as e:
                    print(e)
                try:
                    a_lista.add_row_csv([
                        usuario.get('cre','Sem cre'),
                        usuario.get('municipio','Sem município'),
                        inep,
                        usuario.get('nome','Sem nome'),
                        usuario.get('id','Sem id'),
                        os_dias[0],
                        os_dias[-1],
                        acessou_ultima_semana,
                        len(os_dias),
                        total_atividades,
                        atv_ultimos_sete_dias
                    ])
                except Exception as e:
                    print(e)
                # try:
                #     f= FuncaoDocente()
                #     f.cre = usuario.get('cre','Sem cre')
                #     f.municipio = usuario.get('municipio','Sem município')
                #     f.inep = inep
                #     f.nome = usuario.get('nome','Sem nome')
                #     f.professor_id = usuario.get('id','Sem id')

                #     f.ultimo_acesso = os_dias[0]
                #     f.primeiro_acesso =  os_dias[-1]

                #     f.acessos_ultima_semana = acessou_ultima_semana
                #     f.acessos_desde_inicio = len(os_dias) 
                #     f.total_atividades = total_atividades
                #     f.atividades_ultima_semana = atv_ultimos_sete_dias 

                #     f.save()

                # except Exception as e:
                #     print(e)
                        





    

    
