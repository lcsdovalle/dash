 #pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import UltimoStatusProfessor
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
a_lista = PyCsv('listas/porescola')
#service_class = authService( escopos,'jsons/cred_rs2.json',f"getedu@educar.rs.gov.br").getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    dados = UltimoStatusProfessor.objects.all()
    listagem = {}
    for item in dados:
        if item not in listagem:
            listagem[item.inep] = {}
            listagem[item.inep]['ia'] = item.ia
            listagem[item.inep]['ie'] = item.ie
            listagem[item.inep]['iu'] = item.iu
    
    csv = PyCsv('listagem_escola').get_content()

    for linha in csv:
        try:
            inep = linha[3]
            info = listagem[inep]
            linha.append(info['ia'])
            linha.append(info['ie'])
            linha.append(info['iu'])
            a_lista.add_row_csv(linha)
        except Exception as e:
            print(e)
            pass
                        





    

    
