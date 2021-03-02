#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Aluno,Acessos
from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco
import datetime

if __name__ == "__main__":

    todos = Aluno.objects.all()
    print(len(todos))
    for item in todos:
        item
        if item.inep is None:
            print(f"Aluno {item.nome} apagado por não ter inep")
            item.delete()