import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dashedu.models import RelatorioUsuarios
from pylib.googleadmin import authService
from pylib.pycsv import PyCsv
import datetime
from pytz import timezone
escopos = ['https://www.googleapis.com/auth/admin.reports.usage.readonly']

report_service = authService(escopos,'jsons/cred_sc.json',email='gam@sed.sc.gov.br').getService('admin','reports_v1')

csv = PyCsv('usuarios').get_content()
csv_usuarios = {}
for linha in csv:
    csv_usuarios[linha[0]] = {}
    csv_usuarios[linha[0]]['codigo_usuario'] = linha[0]
    csv_usuarios[linha[0]]['regiao'] = linha[1]
    csv_usuarios[linha[0]]['municipio'] = linha[2]
    csv_usuarios[linha[0]]['inep'] = linha[3]
    csv_usuarios[linha[0]]['codigo_escola'] = linha[4]
    csv_usuarios[linha[0]]['nome_escola'] = linha[5]

if __name__ == "__main__":
    args=[                   
        'accounts:drive_used_quota_in_mb',
        'accounts:first_name',
        'accounts:last_name',
        'accounts:timestamp_last_sso',
        'classroom:num_courses_created',
        'classroom:num_posts_created',
        'classroom:role',
        'classroom:timestamp_last_interaction'
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
                codigo_usuario = perfil.get('userEmail').split('@')[0]
                if codigo_usuario in csv_usuarios:
                    for item in report:
                        if 'courses_created' in item['name']:
                            turmas_criadas = item['intValue']

                        if 'posts_created' in item['name']:
                            posts_criados = item['intValue']

                        if 'role' in item['name']:
                            papel = item.get('stringValue','Não informado')
                            papel = 'Aluno' if papel == 'student' else 'Professor' 

                        if 'classroom:last_interaction_time' == item['name']:
                            ultimo_acesso_classroom = item['datetimeValue']

                        if 'accounts:drive_used_quota_in_mb' == item['name']:
                            uso_drive = item['intValue']

                        if 'accounts:last_name' == item['name']:
                            ultimo_nome = item.get('stringValue','Não informado')

                        if 'accounts:first_name' == item['name']:
                            primeiro_nome = item.get('stringValue','Não informado')

                        if 'accounts:last_sso_time' == item['name']:
                            ultimo_acesso = item['datetimeValue']

                    
                    RelatorioUsuarios.objects.create(
                        data=odia,
                        name="{} {}".format(primeiro_nome.title(),ultimo_nome.title()),
                        uso_drive=uso_drive,
                        ultimo_acesso=ultimo_acesso,
                        turmas_criadas=turmas_criadas,
                        posts_criados=posts_criados,
                        papel=papel,
                        ultimo_acesso_classroom=ultimo_acesso_classroom,
                        codigo_usuario=csv_usuarios[codigo_usuario]['codigo_usuario'],
                        regiao=csv_usuarios[codigo_usuario]['regiao'],
                        municipio=csv_usuarios[codigo_usuario]['municipio'],
                        inep=csv_usuarios[codigo_usuario]['inep'],
                        codigo_escola=csv_usuarios[codigo_usuario]['codigo_escola'],
                        nome_escola=csv_usuarios[codigo_usuario]['nome_escola'],
                    )
                    item
        if len(reports) <1000 or not pagetoken:
            break