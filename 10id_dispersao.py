import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# from dashedu.models import RelatorioUsuarios
from pylib.googleadmin import authService
from pylib.pycsv import PyCsv
import datetime
from pytz import timezone
from dash.models import Escola, IaIndicadorProfessor, IndicadoresGeraisTodaOrganizacao
escopos = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly'
    # 'https://www.googleapis.com/auth/admin.directory.user',
    # 'https://www.googleapis.com/auth/admin.directory.user.readonly',
    # 'https://www.googleapis.com/auth/cloud-platform'
    ]

report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
# admin_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','directory_v1')

if __name__ == "__main__":
    try:
        args=[        
            'classroom:num_1day_students',
            'classroom:num_1day_teachers',        
            'classroom:num_courses_created',        
            'classroom:num_student_posts_created',        
            'classroom:num_teacher_posts_created',        
            'accounts:num_users',
            'meet:num_meetings',
            'meet:num_meetings_web',
            'meet:num_meetings_ios',            
            'meet:num_meetings_android',            
            'meet:total_meeting_minutes',
        ]
        dias = datetime.timedelta(days=3)    
        odia = datetime.date.today() - dias

        report = report_service.customerUsageReports().get(
            date=odia.strftime('%Y-%m-%d'),
            parameters=','.join(args)
        ).execute()

        report = report.get('usageReports',None)
        report = report[0]['parameters'] if report  and 'parameters' in report[0] else report
        professor = 0
        aluno = 0
        usuarios = 0
        turmas = 0
        posts_alunos = 0
        posts_professores = 0
        total_meets = 0
        total_minutos_meets = 0
        total_meets_android = 0
        total_meets_ios = 0
        total_meets_web = 0

        if report:
            for r in report:
                if '1day_teachers' in r['name']:
                    professor = r['intValue']
                
                if '1day_students' in r['name']:
                    aluno = r['intValue']
                
                if 'users' in r['name']:
                    usuarios = r['intValue']
                
                if 'courses' in r['name']:
                    turmas = r['intValue']
                
                if 'student_posts' in r['name']:
                    posts_alunos = r['intValue']
                
                if 'teacher_posts' in r['name']:
                    posts_professores = r['intValue']
                
                if 'meet:num_meetings' == r['name']:
                    total_meets = r['intValue']
                
                if 'meet:num_meetings_web' == r['name']:
                    total_meets_web = r['intValue']
                
                if 'meet:num_meetings_ios' == r['name']:
                    total_meets_ios = r['intValue']
                
                if 'meet:num_meetings_android' == r['name']:
                    total_meets_android = r['intValue']
                
                if 'meet:total_meeting_minutes' == r['name']:
                    total_minutos_meets = r['intValue']
            
            IndicadoresGeraisTodaOrganizacao.objects.create(
                data=odia,
                professores=professor,
                alunos=aluno,
                turmas_criadas=turmas,
                alunos_posts_criados=posts_alunos,
                professores_posts_criados=posts_professores,
                total_meets=total_meets,
                total_meets_android=total_meets_android,
                total_meets_ios=total_meets_ios,
                total_meets_web=total_meets_web,
                total_minutos_meets=total_minutos_meets

                )        

            # TotalUsuarios.objects.create(total=usuarios)
    except Exception as e:
        print(e)