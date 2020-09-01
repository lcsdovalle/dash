import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# from dashedu.models import RelatorioUsuarios
from pylib.googleadmin import authService
from pylib.pycsv import PyCsv
import datetime
from pytz import timezone
from dash.models import Escola, IaIndicadorProfessor, IndicadoresGeraisTodaOrganizacao,Municipios


if __name__ == "__main__":
    escolas = Escola.objects.all()

    for escola in escolas:
        escola.municipio = f"{escola.municipio} - RS"
        escola.save()
