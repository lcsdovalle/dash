#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import Turmas, AlunoEnsalado, NovoIuAluno, NovoIuProfessor
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

#service_class = authService( escopos,'jsons/cred_rs2.json',f"getedu@educar.rs.gov.br").getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    relatorio = PyCsv('lista_iu')
    dados = NovoIuAlunou.objects.all()

    for item in dados:
        relatorio.add_row_csv([
        data 
        inep 
        escola
        municipio
        cre    
        a_um_dia
        a_dois_dias
        a_tres_dias
        a_quatro_dias
        a_cinco_dias = models.IntegerField('Aluno cinco dias')
        a_seis_dias = models.IntegerField('Aluno seis dias')
        a_sete_dias = models.IntegerField('Aluno sete dias')
        a_nenhum_dia = models.IntegerField('Aluno nenhum dia')
        ])
    