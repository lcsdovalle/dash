import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Acessos, Professor, Aluno
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

odia = datetime.datetime.today() - datetime.timedelta(days=1)
odia = odia.strftime('%Y-%m-%d')

if __name__ == "__main__":
    alunos = Aluno.objects.all()
    # * realiza aqui a transferência de OU
    # ll = PyCsv('logs/contas_professores')
    try:
        for usuario in alunos:
            try:
                a = Acessos.objects.create(
                    usuario=usuario.professor_id,
                    acesso= (1 if odia in usuario.ultimo_acesso else 0),
                    data=odia,
                    papel='Professor'
                )
                print(a)
            except Exception as e:
                print(f"Falhou: {e}")
    finally:
        print("Processo concluído")     