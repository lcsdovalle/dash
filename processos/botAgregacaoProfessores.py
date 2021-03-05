#pylint: disable=no-member
from pylib.MyBigQuery import Stream
from google.cloud import bigquery
stream = Stream('getedu-api-293018')
stream.set_client(bigquery.Client()).set_dataset('riograndedosul').set_table('consolidados_professores')

#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import AcessosProfessor, Escola, Professor, Aluno
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
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')

def toStr(valor):
    return valor.strftime('%Y-%m-%d')

def botAgregacaoProfessores():

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    professores = Professor.objects.all()
    escolas = Escola.objects.all()

    todos_professores = {}
    todos_professores_inep = {}

    for professor in professores:
        for inep in professor.inep.split(','):
            if inep not in todos_professores_inep:
                todos_professores_inep[inep] = 1
            else:
                todos_professores_inep[inep] += 1

        todos_professores[professor.email] = {}
        todos_professores[professor.email]['email'] = professor.email
        todos_professores[professor.email]['inep'] = professor.inep
        todos_professores[professor.email]['municipio'] = professor.municipio
        todos_professores[professor.email]['cre'] = professor.cre

    ########################
    # CONSTRÓI OS INTERVALOS 
    ########################

    hoje = datetime.datetime.today() - datetime.timedelta(days=1)

    interval = [
        # hoje - datetime.timedelta(days=7),
        hoje - datetime.timedelta(days=6),
        hoje - datetime.timedelta(days=5),
        hoje - datetime.timedelta(days=4),
        hoje - datetime.timedelta(days=3),
        hoje - datetime.timedelta(days=2),
        hoje - datetime.timedelta(days=1),
        hoje,
        # datetime.datetime.today()
        
    ]
    intervals = list(map(toStr,interval))

    intervalo_menor_sete_dias = {"inicio": hoje - datetime.timedelta(days=6)}
    intervalo_maior_sete_menor_quartorze = {"inicio": hoje - datetime.timedelta(days=14)}
    intervalo_maior_quatorze_menor_trinta = {"inicio": hoje - datetime.timedelta(days=29)}
    intervalo_maior_trinta_menor_sessenta = {"inicio": hoje - datetime.timedelta(days=59)}
    intervalo_maior_sessenta = {"inicio": hoje - datetime.timedelta(days=59)}   

    ########################
    # CONTABILIZA OS DADOS POR USUÁRIOS
    ########################

    reports = AcessosProfessor.objects.all().order_by('-data')[:100]
    contabilizador = {}  
    trava = {}
    quants = {}
    print(len(reports))
    for r in reports:
        user = False
        identificacao_unica_usuario = r.email #pega o email
        adata_acesso = r.data.strftime('%Y-%m-%d') # monta a data para comparação
        

        #verifica se é aluno ou professor
        if identificacao_unica_usuario in todos_professores:    
            user = todos_professores.get(identificacao_unica_usuario)
            role='Professor'
        else:
            continue
        
        # só processa se for aluno
        # agrega o as datas por email
        if user and user['email'] not in contabilizador and user['email'] not in trava:
            odia = datetime.datetime.strptime(adata_acesso,"%Y-%m-%d")
            odia = odia.timestamp()
            contabilizador[user['email']] = {
                    'inep':user['inep'],
                    'cre':user['cre'],
                    'municipio':user['municipio'],
                    'dias':[],
                    'menor_sete': (True if odia >= intervalo_menor_sete_dias['inicio'].timestamp() else False),
                    'maior_sete_menor_quatorze':(True if odia < intervalo_menor_sete_dias['inicio'].timestamp() and odia >= intervalo_maior_sete_menor_quartorze['inicio'].timestamp() else False),
                    'maior_quatorze_menor_trinta':(True if odia < intervalo_maior_sete_menor_quartorze['inicio'].timestamp() and odia >= intervalo_maior_quatorze_menor_trinta['inicio'].timestamp() else False),
                    'maior_trinta_menor_sessenta':(True if odia < intervalo_maior_quatorze_menor_trinta['inicio'].timestamp() and odia >= intervalo_maior_trinta_menor_sessenta['inicio'].timestamp() else False),
                    'maior_sessenta':(True if odia  < intervalo_maior_sessenta['inicio'].timestamp() else False)
                }
            trava[user['email']] = 'processado'

        if user['email'] in contabilizador:
            if adata_acesso not in contabilizador[user['email']]['dias'] and adata_acesso in intervals:
                contabilizador[user['email']]['dias'].append(str(adata_acesso))     
            
    ########################
    # CONTABILIZA OS DADOS POR INEP
    ########################
    for email in contabilizador:
        dados = contabilizador[email]       
        for inep in dados['inep'].split(','):
            if inep not in quants:
                quants[inep] = {}
                
                quants[inep]['menor_sete'] = 1 if dados['menor_sete'] else 0
                quants[inep]['maior_sete_menor_quatorze'] = 1 if dados['maior_sete_menor_quatorze'] else 0
                quants[inep]['maior_quatorze_menor_trinta'] = 1 if dados['maior_quatorze_menor_trinta'] else 0
                quants[inep]['maior_trinta_menor_sessenta'] = 1 if dados['maior_trinta_menor_sessenta'] else 0
                quants[inep]['maior_sessenta'] = 1 if dados['maior_sessenta'] else 0

                quants[inep]['cre'] = dados['cre']
                quants[inep]['municipio'] = dados['municipio']
                quants[inep]['total_logaram'] = 1
                quants[inep]['total_geral'] = todos_professores_inep[inep]

                quants[inep]['p_um_dia'] = 1 if len(dados['dias']) == 1 else 0
                quants[inep]['p_dois_dia'] = 1 if len(dados['dias']) == 2 else 0
                quants[inep]['p_tres_dia'] = 1 if len(dados['dias']) == 3 else 0
                quants[inep]['p_quatro_dia'] = 1 if len(dados['dias']) == 4 else 0
                quants[inep]['p_cinco_dia'] = 1 if len(dados['dias']) == 5 else 0
                quants[inep]['p_seis_dia'] = 1 if len(dados['dias']) == 6 else 0
                quants[inep]['p_sete_dia'] = 1 if len(dados['dias']) == 7 else 0
                quants[inep]['p_nenhum_dia'] = 1 if len(dados['dias']) == 0 else 0

            else:
                if 'menor_sete' not in quants[inep]:
                    quants[inep]['menor_sete'] =  0
                if 'maior_sete_menor_quatorze' not in quants[inep]:
                    quants[inep]['maior_sete_menor_quatorze'] =  0
                if 'maior_quatorze_menor_trinta' not in quants[inep]:
                    quants[inep]['maior_quatorze_menor_trinta'] =  0
                if 'maior_trinta_menor_sessenta' not in quants[inep]:
                    quants[inep]['maior_trinta_menor_sessenta'] =  0
                if 'maior_sessenta' not in quants[inep]:
                    quants[inep]['maior_sessenta'] =  0

                quants[inep]['menor_sete'] += 1 if dados['menor_sete'] else 0
                quants[inep]['maior_sete_menor_quatorze'] += 1 if dados['maior_sete_menor_quatorze'] else 0
                quants[inep]['maior_quatorze_menor_trinta'] += 1 if dados['maior_quatorze_menor_trinta'] else 0
                quants[inep]['maior_trinta_menor_sessenta'] += 1 if dados['maior_trinta_menor_sessenta'] else 0
                quants[inep]['maior_sessenta'] += 1 if dados['maior_sessenta'] else 0
                
                quants[inep]['total_logaram'] += 1
                quants[inep]['total_geral'] = todos_professores_inep[inep]
                
                quants[inep]['p_um_dia'] += 1 if len(dados['dias']) == 1 else 0
                quants[inep]['p_dois_dia'] += 1 if len(dados['dias']) == 2 else 0
                quants[inep]['p_tres_dia'] += 1 if len(dados['dias']) == 3 else 0
                quants[inep]['p_quatro_dia'] += 1 if len(dados['dias']) == 4 else 0
                quants[inep]['p_cinco_dia'] += 1 if len(dados['dias']) == 5 else 0
                quants[inep]['p_seis_dia'] += 1 if len(dados['dias']) == 6 else 0
                quants[inep]['p_sete_dia'] += 1 if len(dados['dias']) == 7 else 0
                quants[inep]['p_nenhum_dia'] += 1 if len(dados['dias']) == 0 else 0


    started=False
    reports = []

    # > um recuo
    ########################
    # Gerar os batchs pra jogar no bigquery
    ########################

    c = 0
    linhas_stream_big_query = {}
    linhas_stream_big_query[c] = []

    hoje = datetime.date.today() #- datetime.timedelta(days=1)
    hoje = hoje.strftime('%Y-%m-%d')

    for inep in quants:
        data = quants[inep]
        escola = escolas.get(inep=inep)
        
        ################################
        ######## BALANCEAMENTO  ########
        ################################
        soma_iu = (
            data['p_um_dia'] +
            data['p_dois_dia'] +
            data['p_tres_dia'] +
            data['p_quatro_dia'] +
            data['p_cinco_dia'] +
            data['p_seis_dia'] +
            data['p_sete_dia']
            )
        quatorze_dias = data['maior_sete_menor_quatorze']
        sete_dias = data['menor_sete']

        if soma_iu != sete_dias:
            if soma_iu > sete_dias:
                resto = soma_iu - sete_dias
                data['menor_sete'] += resto
                data['maior_sete_menor_quatorze'] = data['maior_sete_menor_quatorze'] - resto
            else:
                resto = sete_dias - soma_iu
                data['menor_sete'] = data['menor_sete'] - resto
                data['maior_sete_menor_quatorze'] += resto
        ######## FIM BALANCEAMENTO  ########
        
        
        if len(linhas_stream_big_query[c]) > 500:
            c +=1
            linhas_stream_big_query[c] = []    
            
        try:
            linhas_stream_big_query[c].append({

                "data" : hoje,
                "nome" : escola.nome,
                "nome_cre" : escola.nome_cre,
                "inep" : escola.inep,
                "cre" : escola.cre,
                "municipio" : escola.municipio,

                "menor_sete" : data.get('menor_sete',0),
                "maior_sete_menor_quatorze" : data.get('maior_sete_menor_quatorze',0),
                "maior_quatorze_menor_trinta" : data.get('maior_quatorze_menor_trinta',0),
                "maior_trinta_menor_sessenta" : data.get('maior_trinta_menor_sessenta',0),
                "maior_sessenta" : data.get('maior_sessenta',0),

                #IU
                "p_um_dia" : data.get('p_um_dia',0),
                "p_dois_dias" : data.get('p_dois_dia',0),
                "p_tres_dias" : data.get('p_tres_dia',0),
                "p_quatro_dias" : data.get('p_quatro_dia',0),
                "p_cinco_dias" : data.get('p_cinco_dia',0),
                "p_seis_dias" : data.get('p_seis_dia',0),
                "p_sete_dias" : data.get('p_sete_dia',0),
                "p_nenhum_dia" : data.get('p_sete_dia',0),
                
                
                #IA
                "total_alunos" : data['total_geral'],
                "total_logaram" : data['total_logaram']
            })


        except Exception as e:
            print(e) 


    for item in linhas_stream_big_query:
        info = linhas_stream_big_query[item]

        stream.inserir(info)
        if not stream.errors:
            print("Inserido com sucesso")
        else:
            print(stream.errors)