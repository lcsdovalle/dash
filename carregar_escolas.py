import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from engajamento.models import Escola
from pylib.pycsv import PyCsv

def limpar(valor):    
    valor = valor.strip()
    return valor
if __name__ == "__main__":
    
    escolas = PyCsv('escolas').get_content()

    for escola in escolas:
        try:
            escola = list(map(limpar,escola))
            escola
            e = Escola.objects.create(
                regiao= escola[0],
                municipio= escola[1],
                inep= escola[2],
                email= "{}@sed.sc.gov.br".format(escola[3]),
                nome= escola[4]
            )
            print(e)
        except Exception as e:
            print(e)