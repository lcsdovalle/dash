
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
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

escolas = Escola.objects.all()
relatorio = PyCsv("escolassss")
for escola in escolas:
    idd = "Não localizado"
    try:
        esc = service_admin.users().get(userKey="escola.{}@educar.rs.gov.br".format(escola.inep)).execute()
        idd = esc.get("id")
    except Exception as e:
        pass
    relatorio.add_row_csv([
        escola.nome,
        escola.inep,
        escola.cre,
        escola.nome_cre,
        escola.municipio,
        idd

    ])