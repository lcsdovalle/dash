#CONFIG DJANGO
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

#LIBS
from pylib.MyBigQuery import Stream


from processos.botCarregarEscolas import carregarEscolas

try:
    carregarEscolas()
except Exception as e:
    print(e)