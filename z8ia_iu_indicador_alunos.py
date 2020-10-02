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
from dash.models import Escola, IaIndicadorAluno, Aluno
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
        todos = Aluno.objects.all()
        for usuario in todos:
            if usuario.inep:
                inep = usuario.inep
                E[inep]['total'] += 1    
                E[inep]['logaram'] += 1 if '1970' not in usuario.ultimo_acesso else 0
                E[inep]['logaram_hoje'] +=1 if E[inep]['hoje'] in usuario.ultimo_acesso else 0
                                            
    except Exception as e:
        print(e)
    
    for item in E:
        try:
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
                ia = ( (dados['logaram'] / dados['total'] ) *100 ) if dados['total'] > 0 else 0
            )
        except Exception as er:
            print(er)     
        
