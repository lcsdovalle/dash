import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from engajamento.models import Professor
from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco

ENV_DOMINIO = 'sed.sc.gov.br'
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
    ]
service_admin = authService(
    escopos,
    'jsons/cred_sc.json',
    f"gam@{ENV_DOMINIO}"
    ).getService('admin','directory_v1')

if __name__ == "__main__":
    todos_usuarios = []
    # db = banco("localhost","getedu","getedu00","dashboard_rs")
    # * Só traz de 500 em 500 usuários
    uu = service_admin.users().list(
        customer="my_customer",
        domain='profe.sed.sc.gov.br',
        maxResults=1,                
        projection="full"
        ).execute()
    pageToken = uu.get('nextPageToken',None)
    while True:
        usuarios = service_admin.users().list(
            customer="my_customer",
            domain='profe.sed.sc.gov.br',
            maxResults=500,
            projection="full",
            pageToken=pageToken            
            ).execute()
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
                    p = Professor.objects.create(
                        nome = usuario.get('name').get('fullName'),
                        email = usuario.get('primaryEmail'),
                        ultimo_acesso = usuario.get('lastLoginTime'),
                        professor_id = usuario.get('id')                        
                    )
                    print(p)
                except Exception as e:
                    print(f"Falhou: {e}")
        finally:
            print("Processo concluído")
        if 'nextPageToken' in usuarios:
            pageToken = usuarios.get('nextPageToken',None)
        elif 'nextPageToken' not in usuarios or len(usuarios.get('users')) < 500:
            break
