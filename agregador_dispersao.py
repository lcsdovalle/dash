import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# from dashedu.models import RelatorioUsuarios
from pylib.googleadmin import authService
from pylib.pycsv import PyCsv
import datetime
from pytz import timezone
from dash.models import Acessos,Aluno,Atividade,DispersaoAluno,DispersaoProfessor,IaIndicadorAluno,IaIndicadorProfessor,IndicadorDeFinalDeSemana, Escola

# se todos forem maior que 70 fica verde
# se algum for vai ficar vermelho
# se nao tiver nenhum vermelho e pelo menos um for amarelo será amarelo

# vermelho: abaixo de 50
# amarelo: > 50 < 70
# verde: >70

E = {}
escolas = Escola.objects.all()
dias = datetime.timedelta(days=16)    
odia = datetime.date.today() - dias  
MUNICIPIOS = []
for escola in escolas:
    if escola.municipio not in MUNICIPIOS:
        MUNICIPIOS.append(escola.municipio)
    # escola.status_professor = "N/A"
    # escola.save()
    E[escola.inep] = {}    
    E[escola.inep]['inep'] = escola.inep    
    E[escola.inep]['nome'] = escola.nome    
    E[escola.inep]['municipio'] = escola.municipio    
    E[escola.inep]['cre'] = escola.cre        
    E[escola.inep]['ia_professor'] = 0 
    E[escola.inep]['id_professor'] = 0    
    E[escola.inep]['iu_professor'] = 0    
    E[escola.inep]['ia_aluno'] = 0 
    E[escola.inep]['id_aluno'] = 0    
    E[escola.inep]['iu_aluno'] = 0    

total_municípios = len(MUNICIPIOS)
total_municípios

if __name__ == "__main__":
    #//DATA BASE CALCULO
    domingo = datetime.datetime.today()
    domingo = domingo.strftime('%Y-%m-%d')
    domingo

    #//PROFESSOR
    id_professor = DispersaoProfessor.objects.filter(data=domingo)        
    if len(id_professor) > 0 :
        for item in id_professor:
            E[item.inep]['id_professor'] = item.id_dispersao
    
    ia_professor = IaIndicadorProfessor.objects.filter(data=domingo)        
    if len(ia_professor) > 0 :
        for item in ia_professor:
            E[item.inep]['ia_professor'] = item.ia
    
    iu_professor = IndicadorDeFinalDeSemana.objects.filter(data=domingo)        
    if len(iu_professor) > 0 :
        for item in iu_professor:
            E[item.inep]['iu_professor'] = item.iu_professor

    #//ALUNOR
    id_aluno = DispersaoAluno.objects.filter(data=domingo)        
    if len(id_aluno) > 0 :
        for item in id_aluno:
            E[item.inep]['id_aluno'] = item.id_dispersao
    
    ia_aluno = IaIndicadorAluno.objects.filter(data=domingo)        
    if len(ia_aluno) > 0 :
        for item in ia_aluno:
            E[item.inep]['ia_aluno'] = item.ia
    
    iu_aluno = IndicadorDeFinalDeSemana.objects.filter(data=domingo)        
    if len(iu_aluno) > 0 :
        for item in iu_aluno:
            E[item.inep]['iu_aluno'] = item.iu_aluno
            # E[item.inep]['iu_aluno'] = 78
    
    for linha in E:
        item = E[linha]
        
        aluno = []
        aluno.append(item['ia_aluno'])
        # aluno.append(item['iu_aluno'])
        aluno.append(item['id_aluno'])
        aluno.sort()
        fator_determinante_aluno = aluno[0]

        if fator_determinante_aluno < 40:
            cor_aluno = 'Desenpenho ruim'
        elif fator_determinante_aluno > 40 and fator_determinante_aluno <70:
            cor_aluno = 'Desenpenho aceitável'
        elif fator_determinante_aluno >= 70:
            cor_aluno = 'Desenpenho ideal'

        cor_aluno

        professor = []
        professor.append(item['ia_professor'])
        # professor.append(item['iu_professor'])
        professor.append(item['id_professor'])        
        professor.sort()
        fator_determinante_professor = professor[0]
        
        if fator_determinante_professor < 40:
            cor_prof = 'Desenpenho ruim'
        elif fator_determinante_professor > 40 and fator_determinante_professor <70:
            cor_prof = 'Desenpenho aceitável'
        elif fator_determinante_professor >= 70:
            cor_prof = 'Desenpenho ideal'
        
        cor_prof
        
        try:
            aescola = Escola.objects.get(inep=linha)
            
            aescola.ia_aluno                = item.get('ia_aluno','Não processado')
            aescola.id_aluno                = item.get('ia_aluno','Não processado')
            aescola.iu_aluno                = item.get('ia_aluno','Não processado')
            aescola.status_aluno            = cor_aluno
            
            aescola.ia_professor            = item.get('ia_professor','Não processado')
            aescola.id_professor            = item.get('id_professor','Não processado')
            aescola.iu_professor            = item.get('iu_professor','Não processado')
            aescola.status_professor        = cor_prof
            aescola.latitude                = str(aescola.latitude).replace(',','.')
            aescola.longitude               = str(aescola.longitude).replace(',','.')
            # aescola.save()
        except Exception as e:
            print(e)
    # iu_aluno = iu.iu_aluno
    # iu_professor = iu.iu_professor

    # municipios = {}    

    for muni in MUNICIPIOS:
        escolas_muni = Escola.objects.filter(municipio = muni)
        dividir_por = len(escolas_muni)
        ia_muni_prof = 0
        iu_muni_prof = 0
        id_muni_prof = 0
        ia_muni_aluno = 0
        iu_muni_aluno = 0
        id_muni_aluno = 0
        params_prof = []
        params_aluno = []
        if escolas_muni.exists():
            for esc in escolas_muni:
                ia_muni_prof += esc.ia_professor  
                # iu_muni_prof += esc.iu_professor  
                id_muni_prof += esc.id_professor  

                ia_muni_aluno = esc.ia_aluno  
                # iu_muni_aluno = esc.iu_aluno
                id_muni_aluno = esc.id_aluno

            params_prof.append(ia_muni_prof/dividir_por)
            # params_prof.append(iu_muni_prof/dividir_por)
            params_prof.append(id_muni_prof/dividir_por)            
            params_prof.sort()

            params_aluno.append(ia_muni_aluno/dividir_por)
            # params_aluno.append(iu_muni_aluno/dividir_por)
            params_aluno.append(id_muni_aluno/dividir_por)
            params_aluno.sort()
            
            fator_determinante_professor = params_prof[0]
            if fator_determinante_professor < 40:
                cor_prof = '1'
            elif fator_determinante_professor > 40 and fator_determinante_professor <70:
                cor_prof = '2'
            elif fator_determinante_professor >= 70:
                cor_prof = '3'
            
            fator_determinante_aluno = params_aluno[0]
            if fator_determinante_aluno < 40:
                cor_aluno = '1'
            elif fator_determinante_aluno > 40 and fator_determinante_aluno <70:
                cor_aluno = '2'
            elif fator_determinante_aluno >= 70:
                cor_aluno = '2'            

            for esc in escolas_muni:                
                esc.status_professor = cor_prof
                esc.status_aluno = cor_aluno
                esc.save()


    
