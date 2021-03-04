import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Escola
from pylib.pycsv import PyCsv

def limpar(valor):    
    valor = valor.strip()
    return valor
if __name__ == "__main__":
    
    escolas = PyCsv('logs/csvs/escolas').get_content()

    for escola in escolas:
        try:
            escola = list(map(limpar,escola))
            e = Escola.objects.create(
                cre= escola[0],
                municipio= escola[1],
                inep= escola[2],
                email= "escola.{}@educar.rs.gov.br".format(escola[2]),
                nome= "{} {}".format(escola[3],escola[4])
            )
            print(e)
        except Exception as e:
            print(e)