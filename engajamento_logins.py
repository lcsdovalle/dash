import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from engajamento.models import Atividade, Escola,Turmas, GraficoEngajamento,GraficoAuxiliar


from pylib.spreadsheet import gSheet
from pylib.auth2 import authService
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco
import pymysql
ENV_DOMINIO = 'sed.sc.gov.br'
ENV_LOGGER = PyCsv('grafico1')
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user'      
    ]
service_admin = authService(escopos,'jsons/cred_sc.json',f"gam@sed.sc.gov.br").getService('admin','directory_v1')
usuarios = []
def iniciar_contadores():
    grafico ={}
    escolas = PyCsv('escolass').get_content()   
    
    for e in escolas:
        inep = e[2]    
        grafico[inep] = {} 
        grafico[inep]['regiao'] = e[0]
        grafico[inep]['municipio'] = e[1]
        grafico[inep]['escola_nome'] = "{}".format(e[3])
        grafico[inep]['total_usuarios'] =0
        grafico[inep]['total_usuarios_jalogou']  =0
        grafico[inep]['total_alunos'] =0
        grafico[inep]['total_alunos_jalogou'] =0

    return grafico
if __name__ == "__main__":
    print("Processando...")
    grafico = iniciar_contadores()
    """ GRÁFICOS AUXILIARES"""
    total_educador=0
    total_educadores_jalogou =0        
    total_outros =0
    total_outros_jalogou=0    
        
    retorno = service_admin.users().list(customer="my_customer",maxResults=1).execute()
    pagetoken = retorno.get('nextPageToken')
    usuarios.append(retorno.get("users"))
    while True:
        retorno = service_admin.users().list(customer="my_customer",maxResults=500,pageToken=pagetoken).execute()
        if 'nextPageToken' in retorno:
            pagetoken = retorno.get('nextPageToken')
        if retorno['users'] is not None:
            if len(usuarios) ==1:
                usuarios = usuarios + retorno.get('users')
                usuarios = [usuario for usuario in retorno.get('users')]
            else:
                usuarios = [usuario for usuario in retorno.get('users')]
            for u in usuarios:
                status = "Já logou" if '1970' not in u.get('lastLoginTime') else "Não logou"
                unidade_ou = u.get('orgUnitPath')
                if "organizations" in u:
                    inep = u.get('organizations')[0].get('department') if "organizations" in u else "Não cadastrado"
                    if inep in grafico:
                        grafico[inep]['total_usuarios'] += 1 
                        grafico[inep]['total_usuarios_jalogou'] += 1 if status == "Já logou" else 0
                        grafico[inep]['total_alunos'] += 1 if "Aluno" in unidade_ou else 0
                        grafico[inep]['total_alunos_jalogou'] += 1 if status == "Já logou"  and "Aluno" in unidade_ou else 0
                total_educador += 1 if "Prof" in unidade_ou else 0
                total_educadores_jalogou += 1 if status == "Já logou" and "Profess" in unidade_ou else 0

            if 'nextPageToken' not in retorno:
                break


    for e in grafico:        
        try:
            grafic = GraficoEngajamento.objects.get_or_create(
                inep                = e,
                regiao              = grafico[e].get('regiao'),
                municipio           = grafico[e].get('municipio'),
                escola_nome         = grafico[e].get('escola_nome')
            )[0]

            grafic.total_geral         = grafico[e].get('total_usuarios')
            grafic.jalogaram_total     = grafico[e].get('total_usuarios_jalogou')

            grafic.total_alunos        = grafico[e].get('total_alunos')
            grafic.jalogaram_alunos    = grafico[e].get('total_alunos_jalogou')                
            
            grafic.save()
            

        except Exception as e:
            print(e)
    
    try:
        graf = GraficoAuxiliar.objects.get_or_create(tipo_grafico__exacts='Professores')[0]
        
        graf.total                   = total_educador
        graf.jalogaram_total         = total_educadores_jalogou
        graf.tipo_grafico            = 'Professores'        
        graf.save()
        
    except:
        pass    