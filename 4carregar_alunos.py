#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Aluno,Acessos
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
    todos_usuarios = []    
    uu = service_admin.users().list(customer="my_customer",query='orgUnitPath=/Alunos_nao_ensalados',maxResults=1,projection="full").execute()
    pageToken = uu.get('nextPageToken',None)
    odia = datetime.datetime.today() - datetime.timedelta(days=1)
    odia = odia.strftime('%Y-%m-%d')

    while True:
        try:
            usuarios = service_admin.users().list(customer="my_customer",query='orgUnitPath=/Alunos_nao_ensalados',maxResults=500,projection="full",pageToken=pageToken).execute()
            if len(uu.get('users')) ==1:
                todos_usuarios = uu.get('users') + usuarios.get('users')
            else:
                todos_usuarios = usuarios
                del uu['users']
            
            # * realiza aqui a transferência de OU
            # ll = PyCsv('logs/contas_professores')
            for usuario in todos_usuarios:
                try:
                    organizations = usuario.get('organizations',False)
                    if organizations:
                        organization = organizations[0]
                        inep = organization['department'] if 'department' in organization else False
                        if inep:
                            p = Aluno.objects.get_or_create(
                                aluno_id = usuario.get('id')
                            )[0]
                            p.email = usuario.get('primaryEmail')
                            p.nome = usuario.get('name').get('fullName')
                            p.ultimo_acesso = usuario.get('lastLoginTime').split("T")[0]
                            p.inep = '{}'.format(inep)
                            p.status = 1 if "1970" not in usuario.get("lastLoginTime") else 0
                            p.save()           
                    else:
                        try:
                            p = Aluno.objects.get(
                                aluno_id = usuario.get('id')
                            )
                            
                            p.delete()
                        except Exception as e:
                            # print(e)
                            pass
                except Exception as e:
                    print(f"Falhou: {e}")
        except Exception as e:
            print(e)
        if 'nextPageToken' in usuarios:
            pageToken = usuarios.get('nextPageToken',None)
        elif 'nextPageToken' not in usuarios or len(usuarios.get('users')) < 500:
            break