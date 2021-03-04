#CONFIG DJANGO
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

#LIBS
from pylib.MyBigQuery import Stream


from processos.botCarregarEscolas import carregarEscolas
from processos.botAgregacaoProfessores import botAgregacaoProfessores
from processos.botCarregarProfessores import botCarregarProfessores
from processos.botCarregarAlunos import botCarregarAlunos 

try:
    # carregarEscolas()
    # botCarregarProfessores()
    # botCarregarAlunos()
    botAgregacaoProfessores()
except Exception as e:
    print(e)