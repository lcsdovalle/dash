from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco

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
    db = banco("localhost","getedu","getedu00","dashboard_rs")
    # * Só traz de 500 em 500 usuários
    uu = service_admin.users().list(
        customer="my_customer",
        maxResults=1,        
        query="orgUnitPath=GESTORES(diretores, vices, SSE, SOE, indicados de CRE)",
        projection="full",
        ).execute()
    pageToken = uu.get('nextPageToken',None)
    while True:
        usuarios = service_admin.users().list(
            customer="my_customer",
            maxResults=500,
            projection="full",
            pageToken=pageToken,
            query="orgUnitPath=/Professores"
            ).execute()
        if len(uu.get('users')) ==1:
            todos_usuarios = uu.get('users') + usuarios.get('users')
        else:
            todos_usuarios = usuarios
            del uu['users'] = 0
        
        # * realiza aqui a transferência de OU
        ll = PyCsv('logs/contas_professores')
        try:
            for usuario in todos_usuarios:
                try:
                    params={}    
                    params["nome"] = '{}'.format(usuario.get('name').get('fullName'))
                    params["email"] = '{}'.format(usuario.get('primaryEmail'))
                    params["ultimoacesso"] = '{}'.format(usuario.get('lastLoginTime'))
                    params["id_gsuite"] = '{}'.format(usuario.get('id'))
                    db.tabela('professores').inserir(params)
                    db.executar()

                except Exception as e:
                    print(f"Falhou: {e}")
        finally:
            print("Processo concluído")
        if 'nextPageToken' in usuarios:
            pageToken = usuarios.get('nextPageToken',None)
        elif 'nextPageToken' not in usuarios or len(usuarios.get('users')) < 500:
            break


