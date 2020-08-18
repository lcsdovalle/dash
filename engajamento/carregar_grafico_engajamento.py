import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from engajamento.models import Atividade, Escola,Turmas, GraficoEngajamento,GraficoAuxiliar


from pylib.spreadsheet import gSheet
from pylib.auth2 import authService
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco
import pymysql
ENV_DOMINIO = 'sed.sc.gov.br'
ENV_LOGGER = PyCsv('grafico1')
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user'      
    ]
service_admin = authService(escopos,'jsons/cred_sc.json',f"gam@sed.sc.gov.br").getService('admin','directory_v1')
usuarios = []
def iniciar_contadores():
    grafico ={}
    escolas = PyCsv('escolass').get_content()   
    
    for e in escolas:
        try:
            GraficoEngajamento.objects.create(
                inep                = e[2],
                regiao              = e[0],
                municipio           = e[1],
                escola_nome         = e[3],

                total_geral         = 0,
                jalogaram_total     = 0,

                total_alunos        = 0,
                jalogaram_alunos    = 0
            )
        except:
            pass        
           
    