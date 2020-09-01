import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Acessos
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

odia
if __name__ == "__main__":
    todos_usuarios = []    
    uu = service_admin.users().list(customer="my_customer",query='orgUnitPath=/Alunos',maxResults=1,projection="full").execute()
    pageToken = uu.get('nextPageToken',None)

    while True:
        usuarios = service_admin.users().list(customer="my_customer",query='orgUnitPath=/Alunos',maxResults=500,projection="full",pageToken=pageToken).execute()
        if len(uu.get('users')) ==1:
            todos_usuarios = uu.get('users') + usuarios.get('users')
        else:
            todos_usuarios = usuarios
            del uu['users']
        
        # * realiza aqui a transferência de OU
        # ll = PyCsv('logs/contas_professores')
        try:
            for usuario in todos_usuarios:
                try:
                    a = Acessos.objects.create(
                        usuario=usuario.get('id'),
                        acesso= (1 if odia in usuario['lastLoginTime'] else 0),
                        data=odia,
                        papel='Aluno'
                    )
                    print(a)
                except Exception as e:
                    print(f"Falhou: {e}")
        finally:
            print("Processo concluído")
        if 'nextPageToken' in usuarios:
            pageToken = usuarios.get('nextPageToken',None)
        elif 'nextPageToken' not in usuarios or len(usuarios.get('users')) < 500:
            break