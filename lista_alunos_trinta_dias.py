#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas,NovoDispersaoAluno, NovoIaAluno,NovoIuAluno, NovaAgrecacaoIaAluno, NovoStatusAluno, AlunoEnsalado, NovoIaAluno, NovoStatusAluno, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime

if __name__ == "__main__":

    # MONTA OS CSVS
    resultado = PyCsv("resultado")
    quantitativos = PyCsv("quantitativos")
    consolidado = PyCsv("alunos_mais_trinta_dias")

    # CARREGA NA MEMÓRIA O CADASTRO DOS ALUNOS PROFESSORES E ESCOLAS PARA AGILIZAR
    alunos = Aluno.objects.all()
    todos_alunos = {}
    trinta_dias = datetime.datetime.now() - datetime.timedelta(days=30)
    for aluno in alunos:
        try:
            if '1970' not in str(aluno.ultimo_acesso):
                ultimo_acesso = aluno.ultimo_acesso
                ultimo_acesso = datetime.datetime.strptime(str(ultimo_acesso),'%Y-%m-%d')


                if ultimo_acesso.timestamp() < trinta_dias.timestamp():
                    escol = Escola.objects.get(inep=aluno.inep)
                    consolidado.add_row_csv([
                        aluno.inep,
                        escol.cre,
                        aluno.municipio,
                        aluno.nome,
                        aluno.email,
                        aluno.ultimo_acesso
                        
                    ])
        except Exception as e:
            print(e)
            pass

   


    