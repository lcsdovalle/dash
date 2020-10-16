from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Meet(models.Model):
    data = models.DateField("Data",default=timezone.now)
    codigo_meet = models.CharField("Código do Meet", max_length=50)
    duracao = models.IntegerField("Duração do Meet")
    media = models.IntegerField("Média de Permanência")
    total_usuarios = models.IntegerField("Total de Usuários")
    professores = models.IntegerField("Professores")
    alunos = models.IntegerField("Alunos")
    externos = models.IntegerField("Usuários Externos")
    outros = models.IntegerField("Outros")
    android = models.IntegerField("Usuários Android")
    ios = models.IntegerField("Usuários iOS")
    web = models.IntegerField("Usuários Web")
    desconhecido = models.IntegerField("Dispositivos Desconhecidos")
    cre = models.CharField('CRE', max_length=50)
    municipio = models.CharField('Município', max_length=50)
    inep = models.CharField('INEP', max_length=50)

class DispersaoAluno(models.Model):
    data = models.DateField("Data",default=timezone.now)
    sete_dias = models.BigIntegerField("Sete dias")
    trinta_dias = models.BigIntegerField("Trinta dias")
    sessenta_dias = models.BigIntegerField("Sessenta dias")
    maior_sessenta_dias = models.BigIntegerField("Maior que 60 dias")
    quatorze_dias = models.BigIntegerField("QUatorze dias")
    maior_quatorze_dias = models.BigIntegerField("Maior que 14 dias")
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    nome = models.CharField('Nome', max_length=255)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    id_dispersao = models.BigIntegerField("Indicador de dispersão")

    class Meta:
        verbose_name = ("Dispersão Aluno")
        verbose_name_plural = ("Dispersão Alunos")

class NovoDispersaoAluno(models.Model):
    data = models.DateField("Data",default=timezone.now)
    menor_sete = models.BigIntegerField("Sete dias")
    maior_sete_menor_quatorze = models.BigIntegerField("Maior sete")
    maior_quatorze_menor_trinta = models.BigIntegerField("Maior quatorzer")
    maior_trinta_menor_sessenta = models.BigIntegerField("Maior trinta")
    maior_sessenta = models.BigIntegerField("Maior sessenta")
    
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)


    class Meta:
        verbose_name = ("Dispersão Aluno")
        verbose_name_plural = ("Dispersão Alunos")

class DispersaoProfessor(models.Model):
    data = models.DateField("Data",default=timezone.now)
    sete_dias = models.BigIntegerField("Sete dias")
    trinta_dias = models.BigIntegerField("Trinta dias")
    sessenta_dias = models.BigIntegerField("Sessenta dias")
    maior_sessenta_dias = models.BigIntegerField("Maior que 60 dias")
    quatorze_dias = models.BigIntegerField("Quatorze dias")
    maior_quatorze_dias = models.BigIntegerField("Maior que 14 dias")
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    nome = models.CharField('Nome', max_length=255)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    id_dispersao = models.BigIntegerField("Indicador de dispersão")

    class Meta:
        verbose_name = ("Dispersão Professor")
        verbose_name_plural = ("Dispersão Professores")

class SemanalAtividade(models.Model):
    data = models.DateField("Data",default=timezone.now)
    total_atividades = models.BigIntegerField('Total de Atividades')
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    nome = models.CharField('Nome', max_length=255)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)

    class Meta:
        verbose_name = ("Relatório Semanal de Atividade")
        verbose_name_plural = ("Relatório Semanal de Atividades")

class Escola(models.Model):
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)
    email = models.EmailField('Email', max_length=254,blank=True,null=True,unique=True)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    nome_cre = models.CharField('Nome Cre', max_length=100,blank=True,null=True)    
    latitude = models.CharField('Latitude',max_length=243)
    longitude = models.CharField('Longitude',max_length=243)
    idt = models.CharField('Longitude',max_length=243)
    ia_professor = models.BigIntegerField('Indicador de adoção professor',default=0)
    iu_professor = models.BigIntegerField('Indicador de uso professor',default=0)
    id_professor = models.BigIntegerField('Indicador de dispersão professor',default=0)    
    ia_aluno = models.BigIntegerField('Indicador de adoção professor',default=0)
    iu_aluno = models.BigIntegerField('Indicador de uso professor',default=0)
    id_aluno = models.BigIntegerField('Indicador de dispersão professor',default=0)    
    map_aluno = models.BigIntegerField('Média de atividades produzidas',default=0)    
    ap_aluno = models.BigIntegerField('Atividades produzidas',default=0)    
    status_aluno = models.CharField(
        'Status',
        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            )
        )
    map_professor = models.BigIntegerField('Média de atividades produzidas',default=0)    
    ap_professor = models.BigIntegerField('Atividades produzidas',default=0)    
    status_professor = models.CharField(
        'Status',
        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            )
        )
    
    
    
    class Meta:
        verbose_name = ("Escola")
        verbose_name_plural = ("Escolas")

    def __str_(self):
        return self.nome

class IaIndicadorAluno(models.Model):
    data = models.DateField('Data')
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    total = models.IntegerField('Total')
    acessaram = models.IntegerField('Acessaram')
    logaram_hoje = models.IntegerField('Acessaram Hoje')
    ia = models.BigIntegerField("Indicador de adoção")
    

    class Meta:
        verbose_name = ("IA Aluno")
        verbose_name_plural = ("IA Alunos")

    def __str_(self):
        return self.nome

class IaIndicadorProfessor(models.Model):
    data = models.DateField('Data')
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    total = models.IntegerField('Total')
    acessaram = models.IntegerField('Acessaram')
    logaram_hoje = models.IntegerField('Acessaram Hoje')
    ia = models.BigIntegerField("Indicador de adoção")


    class Meta:
        verbose_name = ("IA Professor")
        verbose_name_plural = ("IA Professores")

    def __str_(self):
        return self.nome

class Turmas(models.Model):
    name = models.CharField("Name", max_length=255,null=True,blank=True)
    turma_id = models.CharField("id", max_length=100,unique=True)
    owner_id = models.CharField('Owner', max_length=100)    
    section = models.CharField('Section', max_length=255,null=True,blank=True)
    owner_email = models.EmailField('Email')
    inep = models.CharField('INEP', max_length=50)    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

    def __str_(self):
        return self.turma_id        

class Atividade(models.Model):
    title = models.CharField('Title', max_length=100,null=True,blank=True)
    atividade_id = models.CharField('ID', max_length=200,unique=True)
    due = models.DateTimeField('Due', auto_now=False, auto_now_add=False,null=True,blank=True)
    state = models.CharField('Course State', max_length=50)
    creator_id = models.CharField('Creator', max_length=100)
    criado = models.CharField('Data criação', max_length=100)
    atualizado = models.CharField('Data atualização', max_length=100)
    turma_id = models.CharField('ID', max_length=200,default='00000')
    inep = models.CharField('INEP', max_length=50)    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = ("Atividade")
        verbose_name_plural = ("Atividades")

    def __str_(self):
        return self.atividade_id

class Professor(models.Model):
    nome = models.CharField('Name', max_length=255, null=True, blank=True)
    email = models.EmailField('Email', max_length=254, null=True, blank=True)
    professor_id = models.CharField('Id', max_length=200,unique=True)
    matricula = models.CharField('Matricula', max_length=50,null=True,blank=True)
    cpf = models.CharField('Cpf', max_length=50,null=True,blank=True)
    ultimo_acesso = models.CharField('Último Acesso', max_length=255, null=True, blank=True)
    inep = models.CharField("Inep",max_length=100, null=True, blank=True)
    status = models.IntegerField("Status", null=True, blank=True)    
    municipio = models.CharField("Município",null=True,blank=True,max_length=254)
    regiao = models.CharField("Região",null=True,blank=True,max_length=254)
    cre = models.CharField("Cre",null=True,blank=True,max_length=254)
    escola = models.CharField("Escola",null=True,blank=True,max_length=254)

    class Meta:
        verbose_name = ("Professor")
        verbose_name_plural = ("Professores")

    def __str_(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField('Name', max_length=255, null=True, blank=True)
    email = models.EmailField('Email', max_length=254, null=True, blank=True)
    aluno_id = models.CharField('Id', max_length=200,unique=True)
    matricula = models.CharField('Matricula', max_length=50, null=True, blank=True)
    cpf = models.CharField('Cpf', max_length=50,null=True, blank=True)
    ultimo_acesso = models.CharField('Último Acesso', max_length=255, null=True, blank=True)
    inep = models.CharField("Inep", max_length=100, null=True, blank=True)
    status = models.IntegerField("Status", null=True, blank=True)
    municipio = models.CharField("Município",null=True,blank=True,max_length=254)
    regiao = models.CharField("Região",null=True,blank=True,max_length=254)
    cre = models.CharField("Cre",null=True,blank=True,max_length=254)
    escola = models.CharField("Escola",null=True,blank=True,max_length=254)    

    class Meta:
        verbose_name = ("Aluno")
        verbose_name_plural = ("Alunos")

    def __str_(self):
        return self.nome

class AlunoEnsalado(models.Model):
    nome = models.CharField('Name', max_length=255, null=True, blank=True)
    email = models.EmailField('Email', max_length=254, null=True, blank=True)
    aluno_id = models.CharField('Id', max_length=200,unique=True)
    matricula = models.CharField('Matricula', max_length=50, null=True, blank=True)
    cpf = models.CharField('Cpf', max_length=50,null=True, blank=True)
    ultimo_acesso = models.CharField('Último Acesso', max_length=255, null=True, blank=True)
    inep = models.CharField("Inep", max_length=100, null=True, blank=True)
    status = models.IntegerField("Status", null=True, blank=True)
    municipio = models.CharField("Município",null=True,blank=True,max_length=254)
    regiao = models.CharField("Região",null=True,blank=True,max_length=254)
    cre = models.CharField("Cre",null=True,blank=True,max_length=254)
    escola = models.CharField("Escola",null=True,blank=True,max_length=254)    

    class Meta:
        verbose_name = ("Aluno")
        verbose_name_plural = ("Alunos")

    def __str_(self):
        return self.nome

class IndicadoresGeraisTodaOrganizacao(models.Model):
    data = models.DateField('Quando', auto_now=False, auto_now_add=False)
    professores = models.BigIntegerField('Professores')
    alunos = models.BigIntegerField('Alunos')
    turmas_criadas = models.BigIntegerField('Número de turmas criadas',default=0)
    alunos_posts_criados = models.BigIntegerField('Número de posts criados por alunos',default=0)
    professores_posts_criados = models.BigIntegerField('Número de posts criados por professores',default=0)
    outros = models.BigIntegerField('Outros',null=True,blank=True)
    total_meets = models.BigIntegerField('Total de meets',null=True,blank=True)
    total_meets_web = models.BigIntegerField('Total meets web',null=True,blank=True)
    total_meets_ios = models.BigIntegerField('Total meets ios',null=True,blank=True)
    total_meets_android = models.BigIntegerField('Total meets android',null=True,blank=True)
    total_minutos_meets = models.BigIntegerField('Total em minutos',null=True,blank=True)
    total_sete_dias = models.BigIntegerField('Total 7 dias',null=True,blank=True)
    total_trinta_dias = models.BigIntegerField('Total 30 dias',null=True,blank=True)
    
class Acessos(models.Model):
    usuario = models.CharField('Nome', max_length=255)
    data = models.DateField('Data')
    acesso = models.IntegerField('Acesso')
    papel = models.CharField('Papel', max_length=50)
    inep = models.CharField("Inep",max_length=100)

class IndicadorDeFinalDeSemana(models.Model):

    data = models.DateField('Data')
    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)
    iu_aluno = models.BigIntegerField("Iu aluno",default=0)
    iu_professor = models.BigIntegerField("Iu professor",default=0)

    p_um_dia = models.IntegerField('Professor um dia')
    p_dois_dias = models.IntegerField('Professor dois dias')
    p_tres_dias = models.IntegerField('Professor tres dias')
    p_quatro_dias = models.IntegerField('Professor quatro dias')
    p_cinco_dias = models.IntegerField('Professor cinco dias')
    p_seis_dias = models.IntegerField('Professor seis dias')
    p_sete_dias = models.IntegerField('Professor sete dias')
    p_nenhum_dia = models.IntegerField('Professor nenhum dia')
    
    a_um_dia = models.IntegerField('Aluno cinco dias')
    a_dois_dias = models.IntegerField('Aluno cinco dias')
    a_tres_dias = models.IntegerField('Aluno cinco dias')
    a_quatro_dias = models.IntegerField('Aluno cinco dias')
    a_cinco_dias = models.IntegerField('Aluno cinco dias')
    a_seis_dias = models.IntegerField('Aluno seois dias')
    a_sete_dias = models.IntegerField('Aluno sete dias')
    a_nenhum_dia = models.IntegerField('Aluno nenhum dia')

class NovoIuAluno(models.Model):

    data = models.DateField('Data')
    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)    
    a_um_dia = models.IntegerField('Aluno um dia')
    a_dois_dias = models.IntegerField('Aluno dois dias')
    a_tres_dias = models.IntegerField('Aluno tres dias')
    a_quatro_dias = models.IntegerField('Aluno quatro dias')
    a_cinco_dias = models.IntegerField('Aluno cinco dias')
    a_seis_dias = models.IntegerField('Aluno seis dias')
    a_sete_dias = models.IntegerField('Aluno sete dias')
    a_nenhum_dia = models.IntegerField('Aluno nenhum dia')

class NovoIuProfessor(models.Model):

    data = models.DateField('Data')
    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)    
    p_um_dia = models.IntegerField('Aluno um dia')
    p_dois_dias = models.IntegerField('Aluno dois dias')
    p_tres_dias = models.IntegerField('Aluno tres dias')
    p_quatro_dias = models.IntegerField('Aluno quatro dias')
    p_cinco_dias = models.IntegerField('Aluno cinco dias')
    p_seis_dias = models.IntegerField('Aluno seis dias')
    p_sete_dias = models.IntegerField('Aluno sete dias')
    p_nenhum_dia = models.IntegerField('Aluno nenhum dia')

class Municipios(models.Model):
    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50,default='Sem nome')
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    nome_cre = models.CharField('Nome Cre', max_length=100,blank=True,null=True)    
    ia_professor = models.BigIntegerField('Indicador de adoção professor',default=0)
    iu_professor = models.BigIntegerField('Indicador de uso professor',default=0)
    id_professor = models.BigIntegerField('Indicador de dispersão professor',default=0)    
    ia_aluno = models.BigIntegerField('Indicador de adoção professor',default=0)
    iu_aluno = models.BigIntegerField('Indicador de uso professor',default=0)
    id_aluno = models.BigIntegerField('Indicador de dispersão professor',default=0)    
    map_aluno = models.BigIntegerField('Média de atividades produzidas',default=0)    
    ap_aluno = models.BigIntegerField('Atividades produzidas',default=0)    
    status_aluno = models.CharField(
        'Status',
        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            )
        )
    map_professor = models.BigIntegerField('Média de atividades produzidas',default=0)    
    ap_professor = models.BigIntegerField('Atividades produzidas',default=0)    
    status_professor = models.CharField(
        'Status',
        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            )
        )

class NovoIaAluno(models.Model):

    data = models.DateField('Data')
    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)    
    total_alunos = models.IntegerField('Aluno um dia')
    total_logaram = models.IntegerField('Aluno dois dias')

class NovoIaPRofessor(models.Model):

    data = models.DateField('Data')
    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)    
    total_alunos = models.IntegerField('Aluno um dia')
    total_logaram = models.IntegerField('Aluno dois dias')

class NovoStatusAluno(models.Model):

    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)    
    total_alunos = models.IntegerField('Aluno um dia',null=True,blank=True)
    total_logaram = models.IntegerField('Aluno dois dias',null=True,blank=True)

class NovoStatusProfessor(models.Model):

    inep = models.CharField("Inep",max_length=100)
    escola = models.CharField("Escola",max_length=100)
    municipio = models.CharField("Município",max_length=100)
    cre = models.CharField("Cre",max_length=100)    
    total_alunos = models.IntegerField('Aluno um dia',null=True,blank=True)
    total_logaram = models.IntegerField('Aluno dois dias',null=True,blank=True)

class NovoDispersaoProfessor(models.Model):

    data = models.DateField("Data",default=timezone.now)
    menor_sete = models.BigIntegerField("Sete dias")
    maior_sete_menor_quatorze = models.BigIntegerField("Maior sete")
    maior_quatorze_menor_trinta = models.BigIntegerField("Maior quatorzer")
    maior_trinta_menor_sessenta = models.BigIntegerField("Maior trinta")
    maior_sessenta = models.BigIntegerField("Maior sessenta")
    
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)


    class Meta:
        verbose_name = ("Dispersão Aluno")
        verbose_name_plural = ("Dispersão Alunos")

class NovaAgrecacaoIaAluno(models.Model):
    data = models.DateField("Data",default=timezone.now)
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)


    total_ensalados = models.BigIntegerField("Total ensalados")
    total_logados = models.BigIntegerField("Total alunos")

class NovoCadastroAtividades(models.Model):
    data = models.DateField("Data",default=timezone.now)
    data_publicacao = models.DateField("Data",default=timezone.now)
    inep = models.CharField('INEP', max_length=50)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    componente_curricular = models.CharField('Componente curricular', max_length=50,blank=True,null=True)
    criador = models.CharField('Criador', max_length=50)

    atividade_id = models.CharField('Atividade Id', max_length=250)
    turma_id = models.CharField('Turma', max_length=250)

    qtd_corrigida = models.BigIntegerField("Corrigidas")
    qtd_nao_iniciada = models.BigIntegerField("Não iniciada")
    qtd_atrasos = models.BigIntegerField("Atrasos")
    qtd_vinculos = models.BigIntegerField("Vínculos")
    qtd_iniciada = models.BigIntegerField("Iniciada",default=0)

class NovaConsolidacaoGeralAluno(models.Model):
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)
    email = models.EmailField('Email', max_length=254,blank=True,null=True,unique=True)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    nome_cre = models.CharField('Nome Cre', max_length=100,blank=True,null=True)   
    
    ia = models.BigIntegerField('Ia',default=0)
    ie = models.BigIntegerField('Ie',default=0)
    iu = models.BigIntegerField('Iu',default=0)
    data = models.DateField("Data",default=timezone.now)
    status_aluno = models.CharField("Cor",        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            ))
    #IE
    menor_sete = models.BigIntegerField("Sete dias")
    maior_sete_menor_quatorze = models.BigIntegerField("Maior sete")
    maior_quatorze_menor_trinta = models.BigIntegerField("Maior quatorzer")
    maior_trinta_menor_sessenta = models.BigIntegerField("Maior trinta")
    maior_sessenta = models.BigIntegerField("Maior sessenta")
    
    
    #IU
    a_um_dia = models.IntegerField('Aluno um dia')
    a_dois_dias = models.IntegerField('Aluno dois dias')
    a_tres_dias = models.IntegerField('Aluno tres dias')
    a_quatro_dias = models.IntegerField('Aluno quatro dias')
    a_cinco_dias = models.IntegerField('Aluno cinco dias')
    a_seis_dias = models.IntegerField('Aluno seis dias')
    a_sete_dias = models.IntegerField('Aluno sete dias')
    a_nenhum_dia = models.IntegerField('Aluno nenhum dia')

    #IA
    total_alunos = models.IntegerField('Aluno um dia')
    total_logaram = models.IntegerField('Aluno dois dias')

class NovaConsolidacaoGeralProfessor(models.Model):
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)
    email = models.EmailField('Email', max_length=254,blank=True,null=True,unique=True)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    nome_cre = models.CharField('Nome Cre', max_length=100,blank=True,null=True)   
    
    data = models.DateField("Data",default=timezone.now)
    ia = models.BigIntegerField('Ia',default=0)
    ie = models.BigIntegerField('Ie',default=0)
    iu = models.BigIntegerField('Iu',default=0)
    #IE
    menor_sete = models.BigIntegerField("Sete dias")
    maior_sete_menor_quatorze = models.BigIntegerField("Maior sete")
    maior_quatorze_menor_trinta = models.BigIntegerField("Maior quatorzer")
    maior_trinta_menor_sessenta = models.BigIntegerField("Maior trinta")
    maior_sessenta = models.BigIntegerField("Maior sessenta")
    status_professor = models.CharField("Cor", default='3',        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            ))
    
    #IU
    p_um_dia = models.IntegerField('Aluno um dia')
    p_dois_dias = models.IntegerField('Aluno dois dias')
    p_tres_dias = models.IntegerField('Aluno tres dias')
    p_quatro_dias = models.IntegerField('Aluno quatro dias')
    p_cinco_dias = models.IntegerField('Aluno cinco dias')
    p_seis_dias = models.IntegerField('Aluno seis dias')
    p_sete_dias = models.IntegerField('Aluno sete dias')
    p_nenhum_dia = models.IntegerField('Aluno nenhum dia')

    #IA
    total_alunos = models.IntegerField('Aluno um dia')
    total_logaram = models.IntegerField('Aluno dois dias')

class UltimoStatusAlunos(models.Model):
    nome = models.CharField('Nome', max_length=255,blank=True,null=True)
    inep = models.CharField('INEP', max_length=50,blank=True,null=True,unique=True)
    email = models.EmailField('Email', max_length=254,blank=True,null=True)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50,blank=True,null=True)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    nome_cre = models.CharField('Nome Cre', max_length=100,blank=True,null=True)   
    
    ia = models.BigIntegerField('Ia',default=0,blank=True,null=True)
    ie = models.BigIntegerField('Ie',default=0,blank=True,null=True)
    iu = models.BigIntegerField('Iu',default=0,blank=True,null=True)
    status_aluno = models.CharField("Cor",        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            )
            ,blank=True,null=True
            )
    #IE
    menor_sete = models.BigIntegerField("Sete dias",blank=True,null=True)
    maior_sete_menor_quatorze = models.BigIntegerField("Maior sete",blank=True,null=True)
    maior_quatorze_menor_trinta = models.BigIntegerField("Maior quatorzer",blank=True,null=True)
    maior_trinta_menor_sessenta = models.BigIntegerField("Maior trinta",blank=True,null=True)
    maior_sessenta = models.BigIntegerField("Maior sessenta",blank=True,null=True)
    
    
    #IU
    a_um_dia = models.IntegerField('Aluno um dia',blank=True,null=True)
    a_dois_dias = models.IntegerField('Aluno dois dias',blank=True,null=True)
    a_tres_dias = models.IntegerField('Aluno tres dias',blank=True,null=True)
    a_quatro_dias = models.IntegerField('Aluno quatro dias',blank=True,null=True)
    a_cinco_dias = models.IntegerField('Aluno cinco dias',blank=True,null=True)
    a_seis_dias = models.IntegerField('Aluno seis dias',blank=True,null=True)
    a_sete_dias = models.IntegerField('Aluno sete dias',blank=True,null=True)
    a_nenhum_dia = models.IntegerField('Aluno nenhum dia',blank=True,null=True)

    #IA
    total_alunos = models.IntegerField('Aluno um dia',blank=True,null=True)
    total_logaram = models.IntegerField('Aluno dois dias',blank=True,null=True)

class UltimoStatusProfessor(models.Model):
    nome = models.CharField('Nome', max_length=255,blank=True,null=True)
    inep = models.CharField('INEP', max_length=50,blank=True,null=True,unique=True)
    email = models.EmailField('Email', max_length=254,blank=True,null=True)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50,blank=True,null=True)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    nome_cre = models.CharField('Nome Cre', max_length=100,blank=True,null=True)   
    
    ia = models.BigIntegerField('Ia',default=0,blank=True,null=True)
    ie = models.BigIntegerField('Ie',default=0,blank=True,null=True)
    iu = models.BigIntegerField('Iu',default=0,blank=True,null=True)
    status_professor = models.CharField("Cor",        max_length=50,
        choices=(
                ('Desenpenho ruim','Desenpenho ruim'),
                ('Desenpenho aceitável','Desenpenho aceitável'),
                ('Desenpenho ideal','Desenpenho ideal')
            )
            ,blank=True,null=True
            )
    #IE
    menor_sete = models.BigIntegerField("Sete dias",blank=True,null=True)
    maior_sete_menor_quatorze = models.BigIntegerField("Maior sete",blank=True,null=True)
    maior_quatorze_menor_trinta = models.BigIntegerField("Maior quatorzer",blank=True,null=True)
    maior_trinta_menor_sessenta = models.BigIntegerField("Maior trinta",blank=True,null=True)
    maior_sessenta = models.BigIntegerField("Maior sessenta",blank=True,null=True)
    
    
    #IU
    p_um_dia = models.IntegerField('Aluno um dia',blank=True,null=True)
    p_dois_dias = models.IntegerField('Aluno dois dias',blank=True,null=True)
    p_tres_dias = models.IntegerField('Aluno tres dias',blank=True,null=True)
    p_quatro_dias = models.IntegerField('Aluno quatro dias',blank=True,null=True)
    p_cinco_dias = models.IntegerField('Aluno cinco dias',blank=True,null=True)
    p_seis_dias = models.IntegerField('Aluno seis dias',blank=True,null=True)
    p_sete_dias = models.IntegerField('Aluno sete dias',blank=True,null=True)
    p_nenhum_dia = models.IntegerField('Aluno nenhum dia',blank=True,null=True)

    #IA
    total_alunos = models.IntegerField('Aluno um dia',blank=True,null=True)
    total_logaram = models.IntegerField('Aluno dois dias',blank=True,null=True)


class FuncaoDocente(models.Model):
    cre = models.CharField("Cre",null=True,blank=True,max_length=254)
    municipio = models.CharField("Município",null=True,blank=True,max_length=254)
    inep = models.CharField("Inep",max_length=100, null=True, blank=True)
    nome = models.CharField('Name', max_length=255, null=True, blank=True)
    email = models.EmailField('Email', max_length=254, null=True, blank=True)
    professor_id = models.CharField('Id', max_length=200)

    ultimo_acesso = models.DateField("Último acesso",default=timezone.now)
    primeiro_acesso = models.DateField("Primeiro acesso",default=timezone.now)
    
    acessos_ultima_semana = models.BigIntegerField("Acessos na última semana",null=True, blank=True)
    acessos_desde_inicio = models.BigIntegerField("Acessos desde inicio",null=True, blank=True) 
    total_atividades = models.BigIntegerField("Total atividades",null=True, blank=True) 
    atividades_ultima_semana = models.BigIntegerField("Atividades última semana",null=True, blank=True) 
    meets_totais = models.BigIntegerField("Meets totais",null=True, blank=True) 
    meets_ultima_semana = models.BigIntegerField("Meets última semana",null=True, blank=True) 
 

