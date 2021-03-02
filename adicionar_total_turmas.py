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

if __name__ == "__main__":
    arquivo = PyCsv('turmas_rs').get_content()

    for linha in arquivo:
        total = linha[5]
        inep = linha[4]

        try:
            objetos = UltimoStatusAlunos.objects.filter(inep=inep)
            if objetos.exists():
                item = objetos[0]
                item.total_turmas = total
                item.save()
        except Exception as e:
            print(e)
            pass
