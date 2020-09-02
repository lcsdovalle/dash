#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# from dashedu.models import RelatorioUsuarios
from pylib.googleadmin import authService
from pylib.pycsv import PyCsv
import datetime
from pytz import timezone
from dash.models import Escola, IaIndicadorAluno
escopos = [
    # 'https://www.googleapis.com/auth/admin.reports.usage.readonly'
    'https://www.googleapis.com/auth/admin.directory.user',
    # 'https://www.googleapis.com/auth/admin.directory.user.readonly',
    # 'https://www.googleapis.com/auth/cloud-platform'
    ]

# report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
admin_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','directory_v1')

if __name__ == "__main__":
    E = {}
    escolas = Escola.objects.all()
    dias = datetime.timedelta(days=1)    
    odia = datetime.date.today() - dias    
    for escola in escolas:
        E[escola.inep] = {}    
        E[escola.inep]['inep'] = escola.inep    
        E[escola.inep]['nome'] = escola.nome    
        E[escola.inep]['municipio'] = escola.municipio    
        E[escola.inep]['cre'] = escola.cre        
        E[escola.inep]['total'] = 0 
        E[escola.inep]['logaram'] = 0    
        E[escola.inep]['hoje'] = odia.strftime('%Y-%m-%d')                        
        E[escola.inep]['logaram_hoje'] = 0    
        

    
    try:
        u = admin_service.users().list(customer='my_customer',query=f"orgUnitPath=/Alunos",maxResults=1,projection='full').execute()

        pagetoken = u.get('nextPageToken',False)

        while(True):
            todos = []
            usuarios = admin_service.users().list(customer='my_customer',query=f"orgUnitPath=/Alunos",maxResults=500,pageToken=pagetoken,projection='full').execute()
            
            del pagetoken

            pagetoken = usuarios.get('nextPageToken',False)

            if u:
                todos = u['users'] + usuarios['users']
            else:
                todos = usuarios['users']
                del u
            
            for usuario in todos:
                usuario
                organizations = usuario.get('organizations',False)
                if organizations:
                    organization = organizations[0]
                    inep = organization['department'] if 'department' in organization else False
                    if inep:
                        E[inep]['total'] += 1    
                        E[inep]['logaram'] += 1 if '1970' not in usuario['lastLoginTime'] else 0
                        E[inep]['logaram_hoje'] +=1 if E[inep]['hoje'] in usuario['lastLoginTime'] else 0
                                                        
            del todos
            if 'nextPageToken' not in usuarios or len(usuarios['users']) <500:
                break
    except Exception as e:
        print(e)
    
    try:
        for item in E:
            dados = E[item]
            dados
            IaIndicadorAluno.objects.create(
                data = odia.strftime('%Y-%m-%d'),
                cre = dados['cre'],
                municipio = dados['municipio'],
                nome = dados['nome'],
                inep = dados['inep'],                        
                total = dados['total'],
                acessaram = dados['logaram'],
                logaram_hoje = dados['logaram_hoje'],                    
            )
    except Exception as er:
        print(er)     
        
