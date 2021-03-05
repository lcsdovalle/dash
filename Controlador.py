#CONFIG DJANGO
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

#LIBS
from pylib.MyBigQuery import Stream


from processos.botCarregarEscolas import carregarEscolas
from processos.botAgregacaoProfessores import botAgregacaoProfessores
from processos.botAgregacaoAlunos import botAgregacaoAlunos
from processos.botCarregarProfessores import botCarregarProfessores
from processos.botCarregarAlunos import botCarregarAlunos 
from processos.botCarregarAcessosProfessores import botCarregarAcessoProfessores 
from processos.botCarregarAcessosAlunos import botCarregarAcessosAlunos
try:
    # carregarEscolas()
    # botCarregarProfessores()
    # botCarregarAlunos()
    # botCarregarAcessoProfessores()
    # botCarregarAcessosAlunos()
    # botAgregacaoAlunos() #pronto pra rodar
    botAgregacaoProfessores()
except Exception as e:
    print(e)