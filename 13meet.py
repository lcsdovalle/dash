#pylint: disable=no-member

import csv
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime

escopos = [
  'https://www.googleapis.com/auth/admin.reports.audit.readonly',
]

report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":
  arq_meet = open("Relatorio Meet.csv", 'w', newline='', encoding='utf-8')
  csv_meet = csv.writer(arq_meet)
  nextPageToken = 1
  professores = Professor.objects.all()
  todos_professores = {}
  for professor in professores:
    todos_professores[professor.email] = {}
    todos_professores[professor.email]['email'] = professor.email
    todos_professores[professor.email]['inep'] = professor.inep
    todos_professores[professor.email]['municipio'] = professor.municipio
    todos_professores[professor.email]['cre'] = professor.cre

  result = report_service.activities().list(applicationName="meet", userKey="all").execute()
  for x in result['items']:
    try:
      email = x['actor']['email']
    except:
      print(x)
      break
    event = x['events'][0]['name']
    data = x['id']['time']
    parameters = x['events'][0]['parameters']
    for y in parameters:
      if y['name'] == 'device_type':
        device = y['value']
      elif y['name'] == 'duration_seconds':
        duration = y['intValue']
      elif y['name'] == 'organizer_email':
        criador = y['value']
      elif y['name'] == 'meeting_code':
        meet_code = y['value']
    if email in todos_professores:
      cre = todos_professores[email]['cre']
      municipio = todos_professores[email]['municipio']
      inep = todos_professores[email]['inep']
      csv_meet.writerow([event, data, email, device, criador, meet_code, duration, cre, municipio, inep])
      arq_meet.flush()
  nextPageToken = result.get("nextPageToken")
  while nextPageToken != None:
    try:
      result = report_service.activities().list(applicationName="meet", userKey="all", pageToken=nextPageToken).execute()
      for x in result['items']:
        email = x['actor']['email']
        event = x['events'][0]['name']
        data = x['id']['time']
        parameters = x['events'][0]['parameters']
        for y in parameters:
          if y['name'] == 'device_type':
            device = y['value']
          elif y['name'] == 'duration_seconds':
            duration = y['intValue']
          elif y['name'] == 'organizer_email':
            criador = y['value']
          elif y['name'] == 'meeting_code':
            meet_code = y['value']
        if email in todos_professores:
          cre = todos_professores[email]['cre']
          municipio = todos_professores[email]['municipio']
          inep = todos_professores[email]['inep']
          csv_meet.writerow([event, data, email, device, criador, meet_code, duration, cre, municipio, inep])
      nextPageToken = result.get("nextPageToken")
    except:
      continue

  for x in result['items']:
    print(x)
    break

  