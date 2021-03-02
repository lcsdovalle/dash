#pylint: disable=no-member

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
    

    ########################
    # GRAVA NO BANCO DE DADOS
    ########################
    print("Agora vai gravar no banco")
    quants
    hoje = datetime.date.today() 
    hoje = hoje.strftime('%Y-%m-%d')
    # hoje = '2020-11-19'
    for inep in quants:
        data = quants[inep]
        cre = escolastodas[inep]["cre"]
        escola = escolas.get(inep=inep)

        soma_iu = (
            data['a_um_dia'] +
            data['a_dois_dia'] +
            data['a_tres_dia'] +
            data['a_quatro_dia'] +
            data['a_cinco_dia'] +
            data['a_seis_dia'] +
            data['a_sete_dia']
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
            Gravar = NovaConsolidacaoGeralAluno()
            Gravar.data = hoje
            Gravar.nome = escola.nome
            Gravar.nome_cre = escola.nome_cre
            Gravar.inep = escola.inep
            Gravar.cre = escola.cre
            Gravar.municipio = escola.municipio

            # ia = models.BigIntegerField('Ia',default=0,null=True,blank=True)
            # ie = models.BigIntegerField('Ie',default=0,null=True,blank=True)
            # iu = models.BigIntegerField('Iu',default=0,null=True,blank=True)
            #IE


            Gravar.menor_sete = data.get('menor_sete',0)
            Gravar.maior_sete_menor_quatorze = data.get('maior_sete_menor_quatorze',0)
            Gravar.maior_quatorze_menor_trinta = data.get('maior_quatorze_menor_trinta',0)
            Gravar.maior_trinta_menor_sessenta = data.get('maior_trinta_menor_sessenta',0)
            Gravar.maior_sessenta = data.get('maior_sessenta',0)

            #IU
            Gravar.a_um_dia = data.get('a_um_dia',0)
            Gravar.a_dois_dias = data.get('a_dois_dia',0)
            Gravar.a_tres_dias = data.get('a_tres_dia',0)
            Gravar.a_quatro_dias = data.get('a_quatro_dia',0)
            Gravar.a_cinco_dias = data.get('a_cinco_dia',0)
            Gravar.a_seis_dias = data.get('a_seis_dia',0)
            Gravar.a_sete_dias = data.get('a_sete_dia',0)
            Gravar.a_nenhum_dia = data.get('a_sete_dia',0)
            
            
            #IA
            Gravar.total_alunos = data['total_geral']
            Gravar.total_logaram =data['total_logaram']
            Gravar.save()


        except Exception as e:
            print(e) 

        try:
            Gravar = ""
            Gravar = UltimoStatusAlunos.objects.get_or_create(inep=escola.inep)[0]
            Gravar.nome = escola.nome
            Gravar.nome_cre = escola.nome_cre
            Gravar.inep = escola.inep
            Gravar.cre = escola.cre
            Gravar.municipio = escola.municipio

            Gravar.menor_sete = data.get('menor_sete',0)
            Gravar.maior_sete_menor_quatorze = data.get('maior_sete_menor_quatorze',0)
            Gravar.maior_quatorze_menor_trinta = data.get('maior_quatorze_menor_trinta',0)
            Gravar.maior_trinta_menor_sessenta = data.get('maior_trinta_menor_sessenta',0)
            Gravar.maior_sessenta = data.get('maior_sessenta',0)

            #IU
            Gravar.a_um_dia = data.get('a_um_dia',0)
            Gravar.a_dois_dias = data.get('a_dois_dia',0)
            Gravar.a_tres_dias = data.get('a_tres_dia',0)
            Gravar.a_quatro_dias = data.get('a_quatro_dia',0)
            Gravar.a_cinco_dias = data.get('a_cinco_dia',0)
            Gravar.a_seis_dias = data.get('a_seis_dia',0)
            Gravar.a_sete_dias = data.get('a_sete_dia',0)
            Gravar.a_nenhum_dia = data.get('a_sete_dia',0)
            
            
            #IA
            Gravar.total_alunos = data['total_geral']
            Gravar.total_logaram =data['total_logaram']
            Gravar.save()

        except Exception as e:
            print(e) 

        try:
            iu =  NovoIuAluno(
                data = hoje, #'2020-11-01', #datetime.datetime.today().strftime('%Y-%m-%d'),
                inep = inep,
                # escola = escola.nome,
                municipio = escola.municipio,
                cre = escola.cre,
                a_um_dia = data.get('a_um_dia',0),
                a_dois_dias = data.get('a_dois_dia',0),
                a_tres_dias = data.get('a_tres_dia',0),
                a_quatro_dias = data.get('a_quatro_dia',0),
                a_cinco_dias = data.get('a_cinco_dia',0),
                a_seis_dias = data.get('a_seis_dia',0),
                a_sete_dias = data.get('a_sete_dia',0),
                a_nenhum_dia = data.get('a_nenhum_dia',0)
            )
            iu
            iu.save()
        except Exception as e:
            print(e)


        try:
            # hoje = datetime.datetime.today()
            # hoje = hoje.strftime('%Y-%m-%d')
            # escola = escolastodas.get(inep=inep)
            NovoDispersaoAluno.objects.create(
                data = hoje,
                menor_sete = data.get('menor_sete',0),
                maior_sete_menor_quatorze = data.get('maior_sete_menor_quatorze',0),
                maior_quatorze_menor_trinta = data.get('maior_quatorze_menor_trinta',0),
                maior_trinta_menor_sessenta = data.get('maior_trinta_menor_sessenta',0),
                maior_sessenta = data.get('maior_sessenta',0),

                inep = inep ,
                cre = cre ,
                municipio = data['municipio'] 
            )
        except Exception as e:
            print(e)
        
        try:            
            novo_ia = NovoIaAluno(
                data = hoje,
                inep = inep,
                cre = cre,
                municipio = data['municipio'],
                total_alunos = data['total_geral'],
                total_logaram = data['total_logaram']
            )
            novo_ia.save()
        except Exception as e:
            print(e)
                    
        try:   
            status = NovoStatusAluno.objects.get_or_create(
                inep = inep ,
                cre = cre ,
                municipio = data['municipio']
            )[0]
            status.total_alunos = data['total_geral']
            status.total_logaram = data['total_logaram']
            status.save()

        except Exception as e:
            print(e)
