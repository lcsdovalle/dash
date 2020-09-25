#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Professor,DispersaoProfessor,Escola
from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco
import datetime
ENV_DOMINIO = 'educar.rs.gov.br'
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
    ]
service_admin = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@{ENV_DOMINIO}"
    ).getService('admin','directory_v1')



if __name__ == "__main__":

    E = {}
    escolas = Escola.objects.all()
    for escola in escolas:
        E[escola.inep] = {}    
        E[escola.inep]['inep'] = escola.inep    
        E[escola.inep]['nome'] = escola.nome    
        E[escola.inep]['municipio'] = escola.municipio   
        E[escola.inep]['regiao'] = escola.regiao 
        E[escola.inep]['cre'] = escola.cre        
        E[escola.inep]['total'] = 0 
        E[escola.inep]['logou_7_dias'] = 0    
        E[escola.inep]['logou_14_dias'] = 0   

        E[escola.inep]['trinta_dias'] = 0    
        E[escola.inep]['sessenta_dias'] = 0    
        E[escola.inep]['nao_logou_60_dias'] = 0    
        
        E[escola.inep]['nao_logou_14_dias'] = 0    

    sete_dias = datetime.datetime.today() - datetime.timedelta(days=7)
    quatorze_dias = datetime.datetime.today() - datetime.timedelta(days=14)
    trinta_dias = datetime.datetime.today() - datetime.timedelta(days=30)
    sessenta_dias = datetime.datetime.today() - datetime.timedelta(days=60)
    todos_usuarios = Professor.objects.all()
    print(len(todos_usuarios))
    for usuario in todos_usuarios:
        ineps = usuario.inep.split(',')
        for inep in ineps:
            try:
                if inep in E:
                    if '1970' not in usuario.ultimo_acesso:
                        datalogin = usuario.ultimo_acesso.split("T")[0]
                        datalogin = datetime.datetime.strptime(datalogin,"%Y-%m-%d")
                        datalogin = datalogin.timestamp()

                        if datalogin >= sete_dias.timestamp():
                            E[inep]['logou_7_dias'] += 1 

                        elif datalogin > quatorze_dias.timestamp():
                            E[inep]['logou_14_dias'] += 1

                            
                        elif datalogin > trinta_dias.timestamp():
                            E[escola.inep]['trinta_dias'] += 1    

                        elif datalogin > sessenta_dias.timestamp():
                            E[escola.inep]['sessenta_dias'] += 1       

                        else:

                            E[inep]['nao_logou_60_dias'] += 1                        
            except:
                E[inep]['nao_logou_14_dias'] += 1

    for escola in E:
        desconto = datetime.timedelta(days=1)
        data = datetime.datetime.today() - desconto
        data = data.strftime('%Y-%m-%d')
        dispersao = DispersaoProfessor.objects.create(
            data = data,
            sete_dias = E[escola]['logou_7_dias'],

            sessenta_dias = E[escola]['sessenta_dias'],
            maior_sessenta_dias = E[escola]['nao_logou_60_dias'],
            trinta_dias = E[escola]['trinta_dias'],

            quatorze_dias = E[escola]['logou_14_dias'],
            maior_quatorze_dias = E[escola]['nao_logou_14_dias'],
            inep = E[escola]['inep'],
            nome = E[escola]['nome'],
            regiao = E[escola]['regiao'],
            municipio = E[escola]['municipio'],
            cre = E[escola]['cre'],
            id_dispersao = (
                ( (  ( E[escola]['logou_7_dias'] + E[escola]['logou_14_dias'] ) / (E[escola]['logou_7_dias'] + E[escola]['logou_14_dias'] + E[escola]['nao_logou_14_dias'] ) ) * 100 ) 
                if (E[escola]['logou_7_dias'] + E[escola]['logou_14_dias'] + E[escola]['nao_logou_14_dias'])>0 else
                0                
            )
        )