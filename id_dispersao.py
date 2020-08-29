import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# from dashedu.models import RelatorioUsuarios
from pylib.googleadmin import authService
from pylib.pycsv import PyCsv
import datetime
from pytz import timezone
from dash.models import Escola, IaIndicadorProfessor
escopos = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly'
    # 'https://www.googleapis.com/auth/admin.directory.user',
    # 'https://www.googleapis.com/auth/admin.directory.user.readonly',
    # 'https://www.googleapis.com/auth/cloud-platform'
    ]

report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
# admin_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','directory_v1')

if __name__ == "__main__":
    E = {}
    escolas = Escola.objects.all()
    for escola in escolas:
        E[escola.inep] = {}    
        E[escola.inep]['inep'] = escola.inep    
        E[escola.inep]['nome'] = escola.nome    
        E[escola.inep]['municipio'] = escola.municipio    
        E[escola.inep]['cre'] = escola.cre        
        E[escola.inep]['total'] = 0 
        E[escola.inep]['logaram'] = 0    

    
    try:
            args=[                   
                'accounts:drive_used_quota_in_mb',
                'accounts:first_name',
                'accounts:last_name',
                'accounts:timestamp_last_sso',
            ]
            dias = datetime.timedelta(days=3)    
            odia = datetime.date.today() - dias
            
            started=False

            while True:
                reports=""
                if not started:
                    reports = report_service.userUsageReport().get(
                        date=odia.strftime('%Y-%m-%d'),
                        userKey='all',
                        parameters=','.join(args)                
                        ).execute()
                    started=True
                    pagetoken = reports.get('nextPageToken')
                else:
                    reports = report_service.userUsageReport().get(
                        date=odia.strftime('%Y-%m-%d'),
                        userKey='all',
                        parameters=','.join(args),
                        pageToken=pagetoken            
                    ).execute()

                    pagetoken = reports.get('nextPageToken',False)

                nome = ""
                ultimo_nome = ""
                primeiro_nome = ""
                uso_drive = 0
                ultimo_acesso = ""
                turmas_criadas = 0
                posts_criados = 0
                papel = 'student'
                ultimo_acesso_classroom = 0    
                
                reports = reports.get('usageReports',None)
                
                if reports:
                    for r in reports:
                        report = r['parameters'] if r  and 'parameters' in r else r
                        perfil = r['entity'] if r  and 'entity' in r else r                        
                        
        
        
    except Exception as e:
        print(e)