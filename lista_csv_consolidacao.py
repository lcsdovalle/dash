#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import Turmas, AlunoEnsalado, NovoDispersaoProfessor,FuncaoDocente, Meet,Atividade, NovoIaPRofessor, NovoStatusProfessor, NovoIuProfessor, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
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
a_lista = PyCsv('consolidacao-por-professores')
#service_class = authService( escopos,'jsons/cred_rs2.json',f"getedu@educar.rs.gov.br").getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    relatorio = PyCsv('relatorio_escola')
    professores = Professor.objects.all()
    escolas = Escola.objects.all()
    alunos_ensalados = AlunoEnsalado.objects.all()
    print(len(alunos_ensalados))
    alunos = Aluno.objects.all()
    todos_alunos = {}
    todos_professores = {}
    inep_professores = {}
    inep_alunos_ensalados = {}
    inep_alunos = {}
    for professor in professores:
        for inepp in professor.inep.split(','):
            if inepp not in inep_professores:
                inep_professores[inepp] = []
            inep_professores[inepp].append({
                "email":professor.email,
                "inep":inepp,
                "municipio":professor.municipio,
                "ultimo_acesso":professor.ultimo_acesso,
                "professor_id":professor.professor_id,
                "email":professor.email
            }) 
   
    for aluno_e in alunos_ensalados:
        if aluno_e.inep not in inep_alunos_ensalados:
            inep_alunos_ensalados[aluno_e.inep] = []
        inep_alunos_ensalados[aluno_e.inep].append({
            "email":aluno_e.email,
            "inep":aluno_e.inep,
            "municipio":aluno_e.municipio,
            "ultimo_acesso":aluno_e.ultimo_acesso,
            "aluno_id":aluno_e.aluno_id,
            "email":aluno_e.email
        }) 
    for aluno in alunos:
        if aluno.inep not in inep_alunos:
            inep_alunos[aluno.inep] = []
        
        inep_alunos[aluno.inep].append({
            "email":aluno.email,
            "inep":aluno.inep,
            "municipio":aluno.municipio,
            "ultimo_acesso":aluno.ultimo_acesso,
            "aluno_id":aluno.aluno_id,
            "email":aluno.email
        }) 

    for escola in escolas:
        try:
            try:
                professores = inep_professores[escola.inep]
            except Exception as e:
                professores = False
            try:
                alunos = inep_alunos[escola.inep] # fazer len dará alunos total
            except Exception as e:
                alunos = False
            try:
                alunos_ensalados = inep_alunos_ensalados[escola.inep] # fazer len dará total de alunos ensalados
            except Exception as e:
                alunos_ensalados = False
            try:
                meets = Meet.objects.filter(inep=escola.inep) #pronto, fazer len 
            except Exception as e:
                meets = []
            
            try:
                atividades = Atividade.objects.filter(inep=escola.inep) #len
            except Exception as e:
                atividades = []
            quinze_dias = datetime.datetime.today() - datetime.timedelta(days=15)
            prof_mais_quinze_dias = 0
            aluno_mais_quinze_dias = 0
            
            profs_ativos = 0
            alunos_ativos = 0
            if not professores:
                profs_ativos = 0
                prof_mais_quinze_dias = 0
                professores = []
            if not alunos:
                alunos_ativos =0
                aluno_mais_quinze_dias =0
                professores = []

            for prof in professores:
                if prof['ultimo_acesso'] is not None:
                    if '1970' not in prof['ultimo_acesso']:
                        profs_ativos +=1
                        adata = prof['ultimo_acesso'].split('T')[0]

                        d_prof_ultimo_acesso = datetime.datetime.strptime(adata,'%Y-%m-%d')

                if d_prof_ultimo_acesso.timestamp() > quinze_dias.timestamp():
                    prof_mais_quinze_dias +=1 # total logaram a menos de 15 dias

            for aluno in alunos:
                if prof['ultimo_acesso'] is not None:
                    if '1970' not in aluno['ultimo_acesso']:
                        alunos_ativos +=1
                        adata = aluno['ultimo_acesso'].split('T')[0]
                        d_aluno_ultimo_acesso = datetime.datetime.strptime(adata,'%Y-%m-%d')

                if d_aluno_ultimo_acesso.timestamp() > quinze_dias.timestamp():
                    aluno_mais_quinze_dias +=1 # total logaram a menos de 15 dias
            

            relatorio.add_row_csv([

                escola.inep,
                escola.nome,
                len(professores),
                profs_ativos,
                prof_mais_quinze_dias,
                len(alunos),
                alunos_ativos,
                aluno_mais_quinze_dias,
                len(atividades),
                len(meets),


            ])
        except Exception as e:
            print(e)