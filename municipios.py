# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
# django.setup()

# # from dashedu.models import RelatorioUsuarios
# from pylib.googleadmin import authService
# from pylib.pycsv import PyCsv
# import datetime
# from pytz import timezone
# from dash.models import Turmas, Escola, IaIndicadorAluno, Aluno, Professor, Acessos, Atividade, DispersaoAluno, DispersaoProfessor, IaIndicadorAluno, IaIndicadorProfessor, IndicadorDeFinalDeSemana, SemanalAtividade

# def get_novo_municipio(valor):
#     csv = PyCsv('logs/escolas').get_content()
#     municipio = False    
#     for linha in csv:
#         if str(linha[0].strip().lower()) == str(valor.strip().lower()):                        
#             return "RS-{}".format(linha[1])
        
#     if not municipio:
#         return "Não encontrado"
# if __name__ == "__main__":
    
#     dados = Escola.objects.all()
#     print(len(dados))
#     for objeto in dados:        
#         try:                                           
#             objeto.nome_cre = get_novo_municipio(objeto.cre)
#             objeto.save() 
#             print(objeto)
#         except Exception as e:
#             print(e)

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
from unidecode import unidecode

if __name__ == "__main__":
    localizacao = PyCsv('listas/localescolas').get_content()
    for local in localizacao:
        try:
            infor = UltimoStatusAlunos.objects.get(inep__exact=local[1])
            lat = local[8].replace(".","")
            lon = local[9].replace(".","")

            lat1 = lat[:3]
            lat2 = lat[3:]

            lon1 = lon[:3]
            lon2 = lon[3:]
            
            lat = ".".join([lat1,lat2])
            lon = ".".join([lon1,lon2])
            infor.lat_lon = "{},{}".format(lat,lon)
            infor.save()
        except Exception as e:
            print(e)