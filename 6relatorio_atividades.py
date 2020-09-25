#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Atividade,SemanalAtividade,Escola
from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco
import datetime
ENV_DOMINIO = 'educar.rs.gov.br'
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
    ]
service_admin = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@{ENV_DOMINIO}"
    ).getService('admin','directory_v1')



if __name__ == "__main__":

    E = {}
    escolas = Escola.objects.all()
    for escola in escolas:
        E[escola.inep] = {}    
        E[escola.inep]['inep'] = escola.inep    
        E[escola.inep]['nome'] = escola.nome
        E[escola.inep]['regiao'] = escola.regiao
        E[escola.inep]['municipio'] = escola.municipio    
        E[escola.inep]['cre'] = escola.cre        
        E[escola.inep]['total_atividades'] = 0
        E[escola.inep]['total_sete'] = 0
        E[escola.inep]['total_quatorze'] = 0

    sete_dias = datetime.datetime.today() - datetime.timedelta(days=7)

    atividades = Atividade.objects.all()
    for atividade in atividades:
        data = atividade.criado.split("T")[0]
        data = datetime.datetime.strptime(data, "%Y-%m-%d")
        data = data.timestamp()
        inep = atividade.inep
        if inep in E:
            E[inep]['total_atividades'] += 1 if data >= sete_dias.timestamp() else 0

    for inep in E:
        atividades = E[inep]['total_atividades']
        relatorio_atividade = SemanalAtividade.objects.create(
            total_atividades = atividades,
            inep = E[inep]['inep'],
            nome = E[inep]['nome'],
            regiao = E[inep]['regiao'],
            municipio = E[inep]['municipio'],
            cre = E[inep]['cre'],
        )