import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dashedu.models import InteracoesClassroomPorTipoUsuario,TotalUsuarios
from pylib.googleadmin import authService
import datetime
from pytz import timezone
escopos = ['https://www.googleapis.com/auth/admin.reports.usage.readonly']

report_service = authService(escopos,'jsons/cred_sc.json',email='gam@sed.sc.gov.br').getService('admin','reports_v1')

if __name__ == "__main__":
    args=[        
        'classroom:num_1day_students',
        'classroom:num_1day_teachers',        
        'classroom:num_courses_created',        
        'classroom:num_student_posts_created',        
        'classroom:num_teacher_posts_created',        
        'accounts:num_users'        
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
    if report:
        for r in report:
            if 'teacher' in r['name']:
                professor = r['intValue']
            if 'student' in r['name']:
                aluno = r['intValue']
            if 'users' in r['name']:
                usuarios = r['intValue']
            if 'courses' in r['name']:
                turmas = r['intValue']
            if 'student_posts' in r['name']:
                posts_alunos = r['intValue']
            if 'teacher_posts' in r['name']:
                posts_professores = r['intValue']
        
        InteracoesClassroomPorTipoUsuario.objects.create(data=odia,professores=professor,alunos=aluno,turmas_criadas=turmas,alunos_posts_criados=posts_alunos,professores_posts_criados=posts_professores)        

        TotalUsuarios.objects.create(total=usuarios)
