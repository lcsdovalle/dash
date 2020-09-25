#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Aluno,Acessos, AlunoEnsalado, Escola
from pylib.spreadsheet import gSheet
from pylib.googleadmin import authService,gSheet
from unidecode import unidecode
from pylib.pycsv import PyCsv
from pylib.mysql_banco import banco
import datetime
from multiprocessing import Pool
ENV_DOMINIO = 'educar.rs.gov.br'
escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly', 
    ]
service_admin = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@{ENV_DOMINIO}"
    ).getService('admin','directory_v1')
service_class = authService(
    escopos,
    'jsons/cred_rs2.json',
    f"getedu@{ENV_DOMINIO}"
    ).getService('classroom','v1')

def execute(usuario):
    try:
        salas = service_class.courses().list(
            studentId = usuario.aluno_id
        ).execute()                                
    
        if len( salas.get('courses') ) > 0:
            p = AlunoEnsalado.objects.get_or_create(
                aluno_id = usuario.aluno_id
            )[0]

            try:
                escola = Escola.objects.get(inep = p.inep)
            except Exception as e:
                print(e)
            p.cre = escola.cre
            p.escola = escola.nome
            p.municipio = escola.municipio
            p.email = usuario.email
            p.nome = usuario.nome
            p.ultimo_acesso = usuario.ultimo_acesso
            p.inep = '{}'.format(usuario.inep)
            p.status = 1 if "1970" not in usuario.ultimo_acesso else 0
            p.save() 
            print("Aluno {} cadastrado pois está em {} turmas".format(p.nome,len(salas.get('courses')) ) )

    except Exception as e:
        print(e)

if __name__ == "__main__":
    pool = Pool(4)
    todos_usuarios = Aluno.objects.all()
    print(len(todos_usuarios))
    resultados = []
    for usuario in todos_usuarios:
        resultados.append(pool.apply_async(execute,(usuario,)))
    pool.close()
    pool.join()

            
            