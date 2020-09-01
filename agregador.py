import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dash.models import Turmas, Atividade,IaIndicadorAluno, Acessos, IndicadorDeFinalDeSemana
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
        datetime.date.today() - datetime.timedelta(days=7),
        datetime.date.today() - datetime.timedelta(days=6),
        datetime.date.today() - datetime.timedelta(days=5),
        datetime.date.today() - datetime.timedelta(days=4),
        datetime.date.today() - datetime.timedelta(days=3),
        datetime.date.today() - datetime.timedelta(days=2),
        datetime.date.today() - datetime.timedelta(days=1),
    ]
    intervalo = list(map(toStr,intervalo))        

    contabilizador = {}    
    for dia in intervalo:                
        dados = Acessos.objects.filter(data=dia)
        for item in dados:            
            contabilizador[item.usuario] = {}
            contabilizador[item.usuario]['total_acessos'] = 0
            contabilizador[item.usuario]['papel'] = item.papel
            contabilizador[item.usuario]['total_acessos'] += 1 if item.acesso == 1 else 0 

    p_um_dia = 0
    p_dois_dias = 0
    p_tres_dias = 0
    p_quatro_dias = 0
    p_cinco_dias = 0
    p_seis_dias = 0
    p_sete_dias = 0

    a_um_dia = 0
    a_dois_dias = 0
    a_tres_dias = 0
    a_quatro_dias = 0
    a_cinco_dias = 0
    a_seis_dias = 0
    a_sete_dias = 0

    for linha in contabilizador:
        indicador = contabilizador[linha]
        
        p_um_dia += 1 if indicador['total_acessos'] == 1 and 'Professor' ==  indicador['papel']  else 0 
        p_dois_dias += 1 if indicador['total_acessos'] == 2 and 'Professor' ==  indicador['papel']  else 0
        p_tres_dias += 1 if indicador['total_acessos'] == 3 and 'Professor' ==  indicador['papel']  else 0 
        p_quatro_dias += 1 if indicador['total_acessos'] == 4 and 'Professor' ==  indicador['papel']  else 0 
        p_cinco_dias += 1 if indicador['total_acessos'] == 5 and 'Professor' ==  indicador['papel']  else 0 
        p_seis_dias += 1 if indicador['total_acessos'] == 6 and 'Professor' ==  indicador['papel']  else 0 
        p_sete_dias += 1 if indicador['total_acessos'] == 7 and 'Professor' ==  indicador['papel']  else 0 
        
        a_um_dia += 1 if indicador['total_acessos'] == 1 and 'Aluno' ==  indicador['papel']  else 0 
        a_dois_dias += 1 if indicador['total_acessos'] == 2 and 'Aluno' ==  indicador['papel']  else 0
        a_tres_dias += 1 if indicador['total_acessos'] == 3 and 'Aluno' ==  indicador['papel']  else 0 
        a_quatro_dias += 1 if indicador['total_acessos'] == 4 and 'Aluno' ==  indicador['papel']  else 0 
        a_cinco_dias += 1 if indicador['total_acessos'] == 5 and 'Aluno' ==  indicador['papel']  else 0 
        a_seis_dias += 1 if indicador['total_acessos'] == 6 and 'Aluno' ==  indicador['papel']  else 0 
        a_sete_dias += 1 if indicador['total_acessos'] == 7 and 'Aluno' ==  indicador['papel']  else 0 

    
    data_corrente = datetime.date.today().strftime('%Y-%m-%d')
    try:
        IndicadorDeFinalDeSemana.objects.create(
            data            = data_corrente,    

            p_um_dia        = p_um_dia,
            p_dois_dias     = p_dois_dias,
            p_tres_dias     = p_tres_dias,
            p_quatro_dias   = p_quatro_dias,
            p_cinco_dias    = p_cinco_dias,
            p_seis_dias     = p_seis_dias,
            p_sete_dias     = p_sete_dias,
            
            a_um_dia        = a_um_dia,
            a_dois_dias     = a_dois_dias,
            a_tres_dias     = a_tres_dias,
            a_quatro_dias   = a_quatro_dias,
            a_cinco_dias    = a_cinco_dias,
            a_seis_dias     = a_seis_dias,
            a_sete_dias     = a_sete_dias
        )

    except Exception as e:
        print(e)


     



    

    
