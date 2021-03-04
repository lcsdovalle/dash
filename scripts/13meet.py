#pylint: disable=no-member

import csv
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Escola, Professor, Aluno, Meet
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

nextPageToken = 1
professores = Professor.objects.all()
todos_professores = {}
for professor in professores:
  todos_professores[professor.email] = {}
  todos_professores[professor.email]['email'] = professor.email
  todos_professores[professor.email]['inep'] = professor.inep
  todos_professores[professor.email]['municipio'] = professor.municipio
  todos_professores[professor.email]['cre'] = professor.cre

alunos = Aluno.objects.all()
todos_alunos = {}
for aluno in alunos:
  todos_alunos[aluno.email] = {}
  todos_alunos[aluno.email]['email'] = aluno.email
  todos_alunos[aluno.email]['inep'] = aluno.inep
  todos_alunos[aluno.email]['municipio'] = aluno.municipio
  todos_alunos[aluno.email]['cre'] = aluno.cre

escolas = Escola.objects.all()
todas_escolas = {}
for escola in escolas:
  inep = escola.inep
  if inep not in todas_escolas:
    todas_escolas[inep] = {}
    todas_escolas[inep]['cre'] = escola.cre
    todas_escolas[inep]['municipio'] = escola.municipio

meets = {}
dia = datetime.date.today() - datetime.timedelta(days=1)
dia = dia.strftime('%Y-%m-%d')
inicio = "{}T00:00:00Z".format(dia)
fim = "{}T23:59:00Z".format(dia)
result = report_service.activities().list(applicationName="meet", userKey="all", startTime=inicio, endTime=fim, maxResults=1000).execute()
nextPageToken = result.get("nextPageToken")
for x in result['items']:
  event = x['events'][0]['name']
  if event == 'call_ended':
    try:
      email = x['actor']['email']
    except Exception:
      email = 'external'
    data = x['id']['time'].split("T")[0]
    parameters = x['events'][0]['parameters']
    for y in parameters:
      if y['name'] == 'duration_seconds':
        duracao = int(y['intValue'])
      elif y['name'] == 'organizer_email':
        criador = y['value']
      elif y['name'] == 'meeting_code':
        meet_code = y['value']
      elif y['name'] == 'device_type':
        device = y['value']
    try:
      if criador in todos_professores:
        if meet_code not in meets:
          meets[meet_code] = {}
          meets[meet_code]['organizador'] = criador
          meets[meet_code]['datas'] = {}
          meets[meet_code]['datas'][data] = {}
          meets[meet_code]['datas'][data]['duracao'] = duracao
          meets[meet_code]['datas'][data]['android'] = 0
          meets[meet_code]['datas'][data]['ios'] = 0
          meets[meet_code]['datas'][data]['web'] = 0
          meets[meet_code]['datas'][data]['desconhecido'] = 0
          try:
            meets[meet_code]['datas'][data][device] += 1
          except Exception:
            meets[meet_code]['datas'][data]['desconhecido'] += 1
          meets[meet_code]['datas'][data]['total_users'] = 1
          meets[meet_code]['datas'][data]['tempo_total'] = duracao
          meets[meet_code]['datas'][data]['media_permanencia'] = duracao
          meets[meet_code]['datas'][data]['professores'] = 0
          meets[meet_code]['datas'][data]['alunos'] = 0
          meets[meet_code]['datas'][data]['externos'] = 0
          meets[meet_code]['datas'][data]['outros'] = 0
          if email in todos_professores:
            meets[meet_code]['datas'][data]['professores'] += 1
          elif email in todos_alunos:
            inep = todos_alunos[email]['inep']
            meets[meet_code]['datas'][data]['alunos'] += 1
            meets[meet_code]['inep'] = inep
            meets[meet_code]['cre'] = todas_escolas[inep]['cre']
            meets[meet_code]['municipio'] = todas_escolas[inep]['municipio']
          elif email == 'external':
            meets[meet_code]['datas'][data]['externos'] += 1
          else:
            meets[meet_code]['datas'][data]['outros'] += 1
        else:
          if data not in meets[meet_code]:
            meets[meet_code]['datas'][data] = {}
            meets[meet_code]['datas'][data]['duracao'] = duracao
            meets[meet_code]['datas'][data]['android'] = 0
            meets[meet_code]['datas'][data]['ios'] = 0
            meets[meet_code]['datas'][data]['web'] = 0
            meets[meet_code]['datas'][data]['desconhecido'] = 0
            try:
              meets[meet_code]['datas'][data][device] += 1
            except Exception:
              meets[meet_code]['datas'][data]['desconhecido'] += 1
            meets[meet_code]['datas'][data]['total_users'] = 1
            meets[meet_code]['datas'][data]['tempo_total'] = duracao
            meets[meet_code]['datas'][data]['media_permanencia'] = duracao
            meets[meet_code]['datas'][data]['professores'] = 0
            meets[meet_code]['datas'][data]['alunos'] = 0
            meets[meet_code]['datas'][data]['externos'] = 0
            meets[meet_code]['datas'][data]['outros'] = 0
            if email in todos_professores:
              meets[meet_code]['datas'][data]['professores'] += 1
            elif email in todos_alunos:
              inep = todos_alunos[email]['inep']
              meets[meet_code]['datas'][data]['alunos'] += 1
              meets[meet_code]['inep'] = inep
              meets[meet_code]['cre'] = todas_escolas[inep]['cre']
              meets[meet_code]['municipio'] = todas_escolas[inep]['municipio']
            elif email == 'external':
              meets[meet_code]['datas'][data]['externos'] += 1
            else:
              meets[meet_code]['datas'][data]['outros'] += 1
          else:
            if duracao >= meets[meet_code]['datas'][data]['duracao']:
              meets[meet_code]['datas'][data]['duracao'] = duracao
            try:
              meets[meet_code]['datas'][data][device] += 1
            except Exception:
              meets[meet_code]['datas'][data]['desconhecido'] += 1
            meets[meet_code]['datas'][data]['total_users'] += 1
            meets[meet_code]['datas'][data]['tempo_total'] += duracao
            meets[meet_code]['datas'][data]['media_permanencia'] = meets[meet_code]['datas'][data]['tempo_total'] / meets[meet_code]['datas'][data]['total_users']
            if email in todos_professores:
              meets[meet_code]['datas'][data]['professores'] += 1
            elif email in todos_alunos:
              inep = todos_alunos[email]['inep']
              meets[meet_code]['datas'][data]['alunos'] += 1
              meets[meet_code]['inep'] = inep
              meets[meet_code]['cre'] = todas_escolas[inep]['cre']
              meets[meet_code]['municipio'] = todas_escolas[inep]['municipio']
            elif email == 'external':
              meets[meet_code]['datas'][data]['externos'] += 1
            else:
              meets[meet_code]['datas'][data]['outros'] += 1
    except NameError:
      print(x)  

while nextPageToken != None:
  try:
    result = report_service.activities().list(applicationName="meet", userKey="all", startTime=inicio, endTime=fim, pageToken=nextPageToken, maxResults=1000).execute()
  except Exception:
    continue
  nextPageToken = result.get("nextPageToken")
  print(nextPageToken)
  for x in result['items']:
    event = x['events'][0]['name']
    if event == 'call_ended':
      try:
        email = x['actor']['email']
      except Exception:
        email = 'external'
      data = x['id']['time'].split("T")[0]
      parameters = x['events'][0]['parameters']
      for y in parameters:
        if y['name'] == 'duration_seconds':
          duracao = int(y['intValue'])
        elif y['name'] == 'organizer_email':
          criador = y['value']
        elif y['name'] == 'meeting_code':
          meet_code = y['value']
        elif y['name'] == 'device_type':
          device = y['value']
      if criador in todos_professores:
        if meet_code not in meets:
          meets[meet_code] = {}
          meets[meet_code]['organizador'] = criador
          meets[meet_code]['datas'] = {}
          meets[meet_code]['datas'][data] = {}
          meets[meet_code]['datas'][data]['duracao'] = duracao
          meets[meet_code]['datas'][data]['android'] = 0
          meets[meet_code]['datas'][data]['ios'] = 0
          meets[meet_code]['datas'][data]['web'] = 0
          meets[meet_code]['datas'][data]['desconhecido'] = 0
          try:
            meets[meet_code]['datas'][data][device] += 1
          except Exception:
            meets[meet_code]['datas'][data]['desconhecido'] += 1
          meets[meet_code]['datas'][data]['total_users'] = 1
          meets[meet_code]['datas'][data]['tempo_total'] = duracao
          meets[meet_code]['datas'][data]['media_permanencia'] = duracao
          meets[meet_code]['datas'][data]['professores'] = 0
          meets[meet_code]['datas'][data]['alunos'] = 0
          meets[meet_code]['datas'][data]['externos'] = 0
          meets[meet_code]['datas'][data]['outros'] = 0
          if email in todos_professores:
            meets[meet_code]['datas'][data]['professores'] += 1
          elif email in todos_alunos:
            inep = todos_alunos[email]['inep']
            meets[meet_code]['datas'][data]['alunos'] += 1
            meets[meet_code]['inep'] = inep
            meets[meet_code]['cre'] = todas_escolas[inep]['cre']
            meets[meet_code]['municipio'] = todas_escolas[inep]['municipio']
          elif email == 'external':
            meets[meet_code]['datas'][data]['externos'] += 1
          else:
            meets[meet_code]['datas'][data]['outros'] += 1
        else:
          if data not in meets[meet_code]['datas']:
            meets[meet_code]['datas'][data] = {}
            meets[meet_code]['datas'][data]['duracao'] = duracao
            meets[meet_code]['datas'][data]['android'] = 0
            meets[meet_code]['datas'][data]['ios'] = 0
            meets[meet_code]['datas'][data]['web'] = 0
            meets[meet_code]['datas'][data]['desconhecido'] = 0
            try:
              meets[meet_code]['datas'][data][device] += 1
            except Exception:
              meets[meet_code]['datas'][data]['desconhecido'] += 1
            meets[meet_code]['datas'][data]['total_users'] = 1
            meets[meet_code]['datas'][data]['tempo_total'] = duracao
            meets[meet_code]['datas'][data]['media_permanencia'] = duracao
            meets[meet_code]['datas'][data]['professores'] = 0
            meets[meet_code]['datas'][data]['alunos'] = 0
            meets[meet_code]['datas'][data]['externos'] = 0
            meets[meet_code]['datas'][data]['outros'] = 0
            if email in todos_professores:
              meets[meet_code]['datas'][data]['professores'] += 1
            elif email in todos_alunos:
              inep = todos_alunos[email]['inep']
              meets[meet_code]['datas'][data]['alunos'] += 1
              meets[meet_code]['inep'] = inep
              meets[meet_code]['cre'] = todas_escolas[inep]['cre']
              meets[meet_code]['municipio'] = todas_escolas[inep]['municipio']
            elif email == 'external':
              meets[meet_code]['datas'][data]['externos'] += 1
            else:
              meets[meet_code]['datas'][data]['outros'] += 1
          else:
            if duracao > meets[meet_code]['datas'][data]['duracao']:
              meets[meet_code]['datas'][data]['duracao'] = duracao
            try:
              meets[meet_code]['datas'][data][device] += 1
            except Exception:
              meets[meet_code]['datas'][data]['desconhecido'] += 1
            meets[meet_code]['datas'][data]['total_users'] += 1
            meets[meet_code]['datas'][data]['tempo_total'] += duracao
            meets[meet_code]['datas'][data]['media_permanencia'] = meets[meet_code]['datas'][data]['tempo_total'] / meets[meet_code]['datas'][data]['total_users']
            if email in todos_professores:
              meets[meet_code]['datas'][data]['professores'] += 1
            elif email in todos_alunos:
              inep = todos_alunos[email]['inep']
              meets[meet_code]['datas'][data]['alunos'] += 1
              meets[meet_code]['inep'] = inep
              meets[meet_code]['cre'] = todas_escolas[inep]['cre']
              meets[meet_code]['municipio'] = todas_escolas[inep]['municipio']
            elif email == 'external':
              meets[meet_code]['datas'][data]['externos'] += 1
            else:
              meets[meet_code]['datas'][data]['outros'] += 1

for x in meets:
  for y in meets[x]['datas']:
    if meets[x]['datas'][y]['alunos'] != 0:
      registro = Meet(
        data = y,
        codigo_meet = x,
        duracao = round(meets[x]['datas'][y]['duracao'] / 60),
        media = round(meets[x]['datas'][y]['media_permanencia'] / 60),
        total_usuarios = meets[x]['datas'][y]['total_users'],
        professores = meets[x]['datas'][y]['professores'],
        alunos = meets[x]['datas'][y]['alunos'],
        externos = meets[x]['datas'][y]['externos'],
        outros = meets[x]['datas'][y]['outros'],
        android = meets[x]['datas'][y]['android'],
        ios = meets[x]['datas'][y]['ios'],
        web = meets[x]['datas'][y]['web'],
        desconhecido = meets[x]['datas'][y]['desconhecido'],
        inep = meets[x]['inep'],
        cre = meets[x]['cre'],
        municipio = meets[x]['municipio']
      )
      registro.save()