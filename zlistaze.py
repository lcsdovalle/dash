#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
from dash.models import Turmas, AlunoEnsalado,NovaConsolidacaoGeralAluno, NovaConsolidacaoGeralProfessor, NovoDispersaoProfessor,FuncaoDocente, Meet,Atividade, NovoIaPRofessor, NovoStatusProfessor, NovoIuProfessor, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola, Professor, Aluno, NovaConsolidacaoGeralProfessor
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime



escopos = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/classroom.courses',
        'https://www.googleapis.com/auth/classroom.courses.readonly', 
        'https://www.googleapis.com/auth/admin.reports.audit.readonly',
    ]

#service_class = authService( escopos,'jsons/cred_rs2.json',f"getedu@educar.rs.gov.br").getService('classroom','v1')
report_service = authService(escopos,'jsons/cred_rs2.json',email='getedu@educar.rs.gov.br').getService('admin','reports_v1')
def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":

    relatorio = PyCsv('lista_consolidada_novembro_alunos')
    escolas = PyCsv("escolas_ensino_medio").get_content()
    consolidado = NovaConsolidacaoGeralAluno.objects.filter()
    ineps_ok = {}
    for e in escolas:
        if e[0] not in ineps_ok:
            ineps_ok[e[0]] = "ok"
    
    for dados in consolidado:
        if dados.inep in ineps_ok:
            relatorio.add_row_csv([
                dados.nome,
                dados.inep,
                dados.email,
                dados.regiao,
                dados.municipio,
                dados.cre,
                dados.nome_cre,   

                dados.data,
                dados.ia,
                dados.ie,
                dados.iu,
                #IE
                dados.menor_sete,
                dados.maior_sete_menor_quatorze,
                dados.maior_quatorze_menor_trinta,
                dados.maior_trinta_menor_sessenta,
                dados.maior_sessenta,
                dados.status_aluno,
                dados.a_um_dia,
                dados.a_dois_dias,
                dados.a_tres_dias,
                dados.a_quatro_dias,
                dados.a_cinco_dias,
                dados.a_seis_dias,
                dados.a_sete_dias,

                #IA
                dados.total_alunos,
                dados.total_logaram 
            ])
   