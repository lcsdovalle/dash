#pylint: disable=no-member
from pylib.MyBigQuery import Stream
from google.cloud import bigquery
stream = Stream('getedu-api-293018')
stream.set_client(bigquery.Client()).set_dataset('riograndedosul').set_table('consolidados_professores')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import AcessosAlunos, Turmas,NovoDispersaoAluno,NovaConsolidacaoGeralAluno, AlunoEnsalado,NovoIuAluno, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno,UltimoStatusAlunos
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

service_class = authService(escopos, 'jsons/cred_rs2.json', f"getedu@educar.rs.gov.br" ).getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')

def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    alunos = Aluno.objects.all()
    escolas = Escola.objects.all()
    escolastodas = {}

    for es in escolas:
        if es.inep not in escolastodas:
            escolastodas[es.inep] = {}
            escolastodas[es.inep]['cre'] = es.cre


    todos_alunos = {}
    todos_alunos_por_inep = {}
    
    for aluno in alunos:
        if aluno.inep not in todos_alunos_por_inep:
            todos_alunos_por_inep[aluno.inep] = 1
        else:
            todos_alunos_por_inep[aluno.inep] += 1


        todos_alunos[aluno.email] = {}
        todos_alunos[aluno.email]['email'] = aluno.email
        todos_alunos[aluno.email]['inep'] = aluno.inep
        todos_alunos[aluno.email]['municipio'] = aluno.municipio
        todos_alunos[aluno.email]['cre'] = aluno.cre
        todos_alunos[aluno.email]['ultimo_acesso'] = aluno.ultimo_acesso
    
    print("Alunos carregados na memória")

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
    reports = AcessosAlunos.objects.all().order_by('-data')
    contabilizador = {}  
    trava = {}
    print(len(reports))
    for r in reports:
        user = False
        identificacao_unica_usuario = r.email #pega o email
        adata_acesso = r.data.strftime('%Y-%m-%d') # monta a data para comparação
        

        #verifica se é aluno ou professor
        if identificacao_unica_usuario in todos_alunos:
            user = todos_alunos.get(identificacao_unica_usuario)
            role = 'Aluno'
        else:
            continue
        
        # só processa se for aluno
        # agrega o as datas por email
        if user and role == 'Aluno':
            if user['email'] not in contabilizador and user['email'] not in trava:
                
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
            
        # > umrecuo
        ########################
        # CONTABILIZA OS DADOS POR INEP
        ########################
        quants = {}
        for email in contabilizador:
            dados = contabilizador[email]

            if dados['inep'] not in quants:
                quants[dados['inep']] = {}
                
                quants[dados['inep']]['menor_sete'] = 1 if dados['menor_sete'] else 0
                quants[dados['inep']]['maior_sete_menor_quatorze'] = 1 if dados['maior_sete_menor_quatorze'] else 0
                quants[dados['inep']]['maior_quatorze_menor_trinta'] = 1 if dados['maior_quatorze_menor_trinta'] else 0
                quants[dados['inep']]['maior_trinta_menor_sessenta'] = 1 if dados['maior_trinta_menor_sessenta'] else 0
                quants[dados['inep']]['maior_sessenta'] = 1 if dados['maior_sessenta'] else 0

                quants[dados['inep']]['cre'] = dados['cre']
                quants[dados['inep']]['municipio'] = dados['municipio']
                quants[dados['inep']]['total_logaram'] = 1
                quants[dados['inep']]['total_geral'] = todos_alunos_por_inep[dados['inep']]

                quants[dados['inep']]['a_um_dia'] = 1 if len(dados['dias']) == 1 else 0
                quants[dados['inep']]['a_dois_dia'] = 1 if len(dados['dias']) == 2 else 0
                quants[dados['inep']]['a_tres_dia'] = 1 if len(dados['dias']) == 3 else 0
                quants[dados['inep']]['a_quatro_dia'] = 1 if len(dados['dias']) == 4 else 0
                quants[dados['inep']]['a_cinco_dia'] = 1 if len(dados['dias']) == 5 else 0
                quants[dados['inep']]['a_seis_dia'] = 1 if len(dados['dias']) == 6 else 0
                quants[dados['inep']]['a_sete_dia'] = 1 if len(dados['dias']) == 7 else 0
                quants[dados['inep']]['a_nenhum_dia'] = 1 if len(dados['dias']) == 0 else 0
                # quants[dados['inep']]['total_logaram'] = 1 if '1970' not in dados['ultimo_acesso'] else 0

            else:
                if 'menor_sete' not in quants[dados['inep']]:
                    quants[dados['inep']]['menor_sete'] =  0
                if 'maior_sete_menor_quatorze' not in quants[dados['inep']]:
                    quants[dados['inep']]['maior_sete_menor_quatorze'] =  0
                if 'maior_quatorze_menor_trinta' not in quants[dados['inep']]:
                    quants[dados['inep']]['maior_quatorze_menor_trinta'] =  0
                if 'maior_trinta_menor_sessenta' not in quants[dados['inep']]:
                    quants[dados['inep']]['maior_trinta_menor_sessenta'] =  0
                if 'maior_sessenta' not in quants[dados['inep']]:
                    quants[dados['inep']]['maior_sessenta'] =  0
                
                quants[dados['inep']]['menor_sete'] += 1 if dados['menor_sete'] else 0
                quants[dados['inep']]['maior_sete_menor_quatorze'] += 1 if dados['maior_sete_menor_quatorze'] else 0
                quants[dados['inep']]['maior_quatorze_menor_trinta'] += 1 if dados['maior_quatorze_menor_trinta'] else 0
                quants[dados['inep']]['maior_trinta_menor_sessenta'] += 1 if dados['maior_trinta_menor_sessenta'] else 0
                quants[dados['inep']]['maior_sessenta'] += 1 if dados['maior_sessenta'] else 0

                quants[dados['inep']]['total_logaram'] += 1
                quants[dados['inep']]['total_geral'] = todos_alunos_por_inep[dados['inep']]
                # quants[dados['inep']]['total_logaram'] = 1 if '1970' not in dados['ultimo_acesso'] else 0

                #BUG 
                # if label == 'menor_sete':
                quants[dados['inep']]['a_um_dia'] += 1 if len(dados['dias']) == 1 else 0
                quants[dados['inep']]['a_dois_dia'] += 1 if len(dados['dias']) == 2 else 0
                quants[dados['inep']]['a_tres_dia'] += 1 if len(dados['dias']) == 3 else 0
                quants[dados['inep']]['a_quatro_dia'] += 1 if len(dados['dias']) == 4 else 0
                quants[dados['inep']]['a_cinco_dia'] += 1 if len(dados['dias']) == 5 else 0
                quants[dados['inep']]['a_seis_dia'] += 1 if len(dados['dias']) == 6 else 0
                quants[dados['inep']]['a_sete_dia'] += 1 if len(dados['dias']) == 7 else 0
                quants[dados['inep']]['a_nenhum_dia'] += 1 if len(dados['dias']) == 0 else 0



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

        
            try:
                linhas_stream_big_query.append({

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
                    "total_logaram" : data['total']
                })


            except Exception as e:
                print(e) 