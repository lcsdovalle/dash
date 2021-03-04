import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Escola
from pylib.pycsv import PyCsv

def limpar(valor):    
    valor = valor.strip()
    return valor
def carregarEscolas():
    
    escolas = PyCsv('csvs/escolas').get_content()

    for escola in escolas:
        try:
            escola = list(map(limpar,escola))
            escola
            e = Escola.objects.create(
                cre= escola[0],
                municipio= escola[2],
                inep= escola[1],
                email= "escola.{}@educar.rs.gov.br".format(escola[1]),
                nome= "{} {}".format(escola[6],escola[7])
            )
            print(e)
        except Exception as e:
            print(e)