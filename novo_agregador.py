#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import UltimoStatusAlunos, UltimoStatusProfessor
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime
from io import StringIO
import json
from decimal import Decimal
escopos = [
        'https://www.googleapis.com/auth/admin.reports.audit.readonly'
    ]
# service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":
    
    ## SEPARA APENAS AS ESCOLAS ESTADUAIS
    file = open('geojsons/escolas.geojson', 'r',encoding='utf-8').read()
    io = StringIO(file)
    arquivo = json.load(io)

    dados = arquivo['features'][0]['properties']
    c=0
    novo = []
    for linha in arquivo['features']:
        linha = linha['properties']
        comparacao = linha['mantenedora']
        inep = linha['cod_inep']
        if 'estadual'.lower() == str(comparacao.lower()) or 'estadual'.lower() in str(comparacao.lower()):
            linha['iap'] = 0
            linha['iep'] = 0
            linha['iup'] = 0
            
            linha['iaa'] = 0
            linha['iea'] = 0
            linha['iua'] = 0

            d_a = UltimoStatusProfessor.objects.filter(inep = inep)
            if d_a.exists():
                d_a = d_a[0]
                linha['iap'] = ( (d_a.total_logaram/d_a.total_alunos) *100) if d_a.total_alunos > 0 else 0
                
                r = (d_a.menor_sete+d_a.maior_sete_menor_quatorze+d_a.maior_quatorze_menor_trinta+d_a.maior_trinta_menor_sessenta+d_a.maior_sessenta)
                if r > 0 :
                    linha['iep'] = ((d_a.menor_sete+d_a.maior_sete_menor_quatorze) / r )*100
                
                rr = (d_a.p_um_dia+d_a.p_dois_dias+d_a.p_tres_dias+d_a.p_quatro_dias+d_a.p_cinco_dias+d_a.p_seis_dias+d_a.p_sete_dias)
                ii = (d_a.p_dois_dias+d_a.p_tres_dias+d_a.p_quatro_dias+d_a.p_cinco_dias+d_a.p_seis_dias+d_a.p_sete_dias)
                if rr > 0:
                    linha['iup'] = (ii/rr)*100
            
            d_a = UltimoStatusAlunos.objects.filter(inep = inep)
            if d_a.exists():
                d_a = d_a[0]
                linha['iaa'] = ( (d_a.total_logaram/d_a.total_alunos) *100) if d_a.total_alunos > 0 else 0
                
                r = (d_a.menor_sete+d_a.maior_sete_menor_quatorze+d_a.maior_quatorze_menor_trinta+d_a.maior_trinta_menor_sessenta+d_a.maior_sessenta)
                if r > 0 :
                    linha['iea'] = ((d_a.menor_sete+d_a.maior_sete_menor_quatorze) / r )*100
                
                rr = (d_a.a_um_dia+d_a.a_dois_dias+d_a.a_tres_dias+d_a.a_quatro_dias+d_a.a_cinco_dias+d_a.a_seis_dias+d_a.a_sete_dias)
                ii = (d_a.a_dois_dias+d_a.a_tres_dias+d_a.a_quatro_dias+d_a.a_cinco_dias+d_a.a_seis_dias+d_a.a_sete_dias)
                if rr > 0:
                    linha['iua'] = (ii/rr)*100
                



            novo.append(linha)
        c +=1
    
    arquivo['features'] = novo
    with open('geojsons/data.geojson', 'w') as outfile:
        json.dump(arquivo, outfile)
    


    
    