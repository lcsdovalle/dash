#pylint: disable=no-member

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana,Escola
from pylib.googleadmin import authService
from pylib.mysql_banco import banco
from multiprocessing import Pool
from pylib.pycsv import PyCsv
from pylib.removeBarraN import removeBarraN
import datetime
escopos = [
        'https://www.googleapis.com/auth/classroom.courses',
        # 'https://www.googleapis.com/auth/classroom.courses.readonly',
        # 'https://www.googleapis.com/auth/classroom.rosters',
        # 'https://www.googleapis.com/auth/classroom.profile.emails',
        # 'https://www.googleapis.com/auth/classroom.profile.photos',
        'https://www.googleapis.com/auth/classroom.coursework.students',
        'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        'https://www.googleapis.com/auth/classroom.coursework.me',
        'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    ]
service_class = authService(escopos,'jsons/cred_rs2.json','getedu@educar.rs.gov.br').getService('classroom','v1')

def toStr(valor):
    return valor.strftime('%Y-%m-%d')

if __name__ == "__main__":
    hoje = datetime.datetime.today()    
    intervalo = [
        datetime.date.today() - datetime.timedelta(days=10),
        datetime.date.today() - datetime.timedelta(days=9),
        datetime.date.today() - datetime.timedelta(days=8),
        datetime.date.today() - datetime.timedelta(days=7),
        datetime.date.today() - datetime.timedelta(days=6),
        datetime.date.today() - datetime.timedelta(days=5),
        datetime.date.today() - datetime.timedelta(days=4),
    ]
    intervalo = list(map(toStr,intervalo))        

    contabilizador = {}    
    for dia in intervalo:                
        dados = Acessos.objects.filter(data=dia)
        for item in dados:
            if item.usuario not in contabilizador:            
                contabilizador[item.usuario] = {}
                contabilizador[item.usuario]['total_acessos'] = 0
                contabilizador[item.usuario]['total_acessos'] += 1 if item.acesso == 1 else 0
                contabilizador[item.usuario]['inep'] = item.inep
                contabilizador[item.usuario]['papel'] = item.papel
            else:
                contabilizador[item.usuario]['papel'] = item.papel
                contabilizador[item.usuario]['total_acessos'] += 1 if item.acesso == 1 else 0

    ineps = {}
    for linha in contabilizador:
        indicador = contabilizador[linha]
        for inep in indicador['inep'].split(","):
            if inep not in ineps:
                ineps[inep] = {}
                ineps[inep]['p_um_dia'] = 1 if indicador['total_acessos'] == 1 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_dois_dias'] = 1 if indicador['total_acessos'] == 2 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_tres_dias'] = 1 if indicador['total_acessos'] == 3 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_quatro_dias'] = 1 if indicador['total_acessos'] == 4 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_cinco_dias'] = 1 if indicador['total_acessos'] == 5 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_seis_dias'] = 1 if indicador['total_acessos'] == 6 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_sete_dias'] = 1 if indicador['total_acessos'] == 7 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_nenhum_dia'] = 1 if indicador['total_acessos'] == 0 and 'Professor' ==  indicador['papel'].title()  else 0

                ineps[inep]['a_um_dia'] = 1 if indicador['total_acessos'] == 1 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_dois_dias'] = 1 if indicador['total_acessos'] == 2 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_tres_dias'] = 1 if indicador['total_acessos'] == 3 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_quatro_dias'] = 1 if indicador['total_acessos'] == 4 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_cinco_dias'] = 1 if indicador['total_acessos'] == 5 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_seis_dias'] = 1 if indicador['total_acessos'] == 6 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_sete_dias'] = 1 if indicador['total_acessos'] == 7 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_nenhum_dia'] = 1 if indicador['total_acessos'] == 0 and 'Aluno' ==  indicador['papel'].title()  else 0 
            else:
                ineps[inep]['p_um_dia'] += 1 if indicador['total_acessos'] == 1 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_dois_dias'] += 1 if indicador['total_acessos'] == 2 and 'Professor' ==  indicador['papel'].title()  else 0
                ineps[inep]['p_tres_dias'] += 1 if indicador['total_acessos'] == 3 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_quatro_dias'] += 1 if indicador['total_acessos'] == 4 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_cinco_dias'] += 1 if indicador['total_acessos'] == 5 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_seis_dias'] += 1 if indicador['total_acessos'] == 6 and 'Professor' ==  indicador['papel'].title()  else 0 
                ineps[inep]['p_sete_dias'] += 1 if indicador['total_acessos'] == 7 and 'Professor' ==  indicador['papel'].title()  else 0         
                ineps[inep]['p_nenhum_dia'] += 1 if indicador['total_acessos'] == 0 and 'Professor' ==  indicador['papel'].title()  else 0         
                
                ineps[inep]['a_um_dia'] += 1 if indicador['total_acessos'] == 1 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_dois_dias'] += 1 if indicador['total_acessos'] == 2 and 'Aluno' ==  indicador['papel'].title()  else 0
                ineps[inep]['a_tres_dias'] += 1 if indicador['total_acessos'] == 3 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_quatro_dias'] += 1 if indicador['total_acessos'] == 4 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_cinco_dias'] += 1 if indicador['total_acessos'] == 5 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_seis_dias'] += 1 if indicador['total_acessos'] == 6 and 'Aluno' ==  indicador['papel'].title()  else 0 
                ineps[inep]['a_sete_dias'] += 1 if indicador['total_acessos'] == 7 and 'Aluno' ==  indicador['papel'].title()  else 0         
                ineps[inep]['a_nenhum_dia'] += 1 if indicador['total_acessos'] == 0 and 'Aluno' ==  indicador['papel'].title()  else 0           

    desconto = datetime.timedelta(days=1)

    data_corrente = datetime.date.today() - desconto
    data_corrente = data_corrente.strftime('%Y-%m-%d')    
    try:
        for inep in ineps:
            escola = Escola.objects.get(inep=inep)
            total_alunos = ineps[inep]['a_um_dia'] + ineps[inep]['a_dois_dias'] + ineps[inep]['a_tres_dias'] + ineps[inep]['a_quatro_dias'] + ineps[inep]['a_cinco_dias'] + ineps[inep]['a_seis_dias'] + ineps[inep]['a_sete_dias'] 
            total_professores = ineps[inep]['p_um_dia'] + ineps[inep]['p_dois_dias'] + ineps[inep]['p_tres_dias'] + ineps[inep]['p_quatro_dias'] + ineps[inep]['p_cinco_dias'] + ineps[inep]['a_seis_dias'] + ineps[inep]['a_sete_dias']

            IndicadorDeFinalDeSemana.objects.create(
                inep            = inep,
                escola          = escola.nome,
                cre             = escola.cre,
                municipio       = escola.municipio,

                data            = data_corrente,    

                p_um_dia        = ineps[inep]['p_um_dia'],
                p_dois_dias     = ineps[inep]['p_dois_dias'],
                p_tres_dias     = ineps[inep]['p_tres_dias'],
                p_quatro_dias   = ineps[inep]['p_quatro_dias'],
                p_cinco_dias    = ineps[inep]['p_cinco_dias'],
                p_seis_dias     = ineps[inep]['p_seis_dias'],
                p_sete_dias     = ineps[inep]['p_sete_dias'],
                p_nenhum_dia    = ineps[inep]['p_nenhum_dia'],
                
                a_um_dia        = ineps[inep]['a_um_dia'],
                a_dois_dias     = ineps[inep]['a_dois_dias'],
                a_tres_dias     = ineps[inep]['a_tres_dias'],
                a_quatro_dias   = ineps[inep]['a_quatro_dias'],
                a_cinco_dias    = ineps[inep]['a_cinco_dias'],
                a_seis_dias     = ineps[inep]['a_seis_dias'],
                a_sete_dias     = ineps[inep]['a_sete_dias'],
                a_nenhum_dia    = ineps[inep]['a_nenhum_dia'],   

                iu_aluno = ( (  ( ineps[inep]['a_tres_dias'] + ineps[inep]['a_quatro_dias'] + ineps[inep]['a_cinco_dias'] + ineps[inep]['a_seis_dias'] + ineps[inep]['a_sete_dias'] ) / total_alunos )  *100 ) if total_alunos > 0 else 0,
                iu_professor = ( (  (ineps[inep]['p_tres_dias'] + ineps[inep]['p_quatro_dias'] + ineps[inep]['p_cinco_dias'] + ineps[inep]['p_seis_dias'] + ineps[inep]['p_sete_dias'] ) / total_professores ) *100  ) if total_professores > 0 else 0

        )

    except Exception as e:
        print(e)


     



    

    
