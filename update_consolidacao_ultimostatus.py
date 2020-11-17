#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, UltimoStatusAlunos, UltimoStatusProfessor, NovaAgrecacaoIaAluno, NovaConsolidacaoGeralAluno, NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime
from unidecode import unidecode

def backup():

    dados = UltimoStatusAlunos.objects.all() 
    dadosc = NovaConsolidacaoGeralAluno.objects.all()
    
    for item in dadosc:
        if item.total_alunos > 0:

            item.ia = int((item.total_logaram / item.total_alunos) * 100)
            item.save()

if __name__ == "__main__":

    dados = UltimoStatusProfessor.objects.all()
    arquivo = PyCsv('local-municipios-rs').get_content()
    for linha in arquivo:
        nome = linha[0]
        latlon = linha[3].replace('"','')
        try:
            r = dados.filter(municipio=f"RS-{str(nome)}")
            if r.exists():
                for item in r:
                    item.lat_lon = latlon
                    item.save()
                
            else:
                print(f"{nome} não localizado")
        except Exception as e:
            print(f"{nome} não encontrado")
