from django.db import models

# Create your models here.

class Escola(models.Model):
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)
    email = models.EmailField('Email', max_length=254,blank=True,null=True,unique=True)
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    
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
    nome = models.CharField('Name', max_length=255)
    email = models.EmailField('Email', max_length=254,unique=True)
    professor_id = models.CharField('Id', max_length=200,unique=True)
    matricula = models.CharField('Matricula', max_length=50,null=True,blank=False)
    cpf = models.CharField('Cpf', max_length=50,null=True,blank=False)
    ultimo_acesso = models.CharField('Ultimo acesso', max_length=100)
    inep = models.CharField("Inep",max_length=100)

    class Meta:
        verbose_name = ("Professor")
        verbose_name_plural = ("Professores")

    def __str_(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField('Name', max_length=255)
    email = models.EmailField('Email', max_length=254,unique=True)
    aluno_id = models.CharField('Id', max_length=200,unique=True)
    matricula = models.CharField('Matricula', max_length=50,null=True,blank=False)
    cpf = models.CharField('Cpf', max_length=50,null=True,blank=False)
    ultimo_acesso = models.CharField('Ultimo acesso', max_length=100)
    inep = models.CharField("Inep", max_length=100)

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

class Municipios(models.Model):
    codigo_ibge = models.BigIntegerField('Código Ibge') 
    nome = models.CharField('Nome', max_length=254)   
    latitude = models.CharField('Latitude', max_length=50)
    longitude = models.CharField('Longitude', max_length=50)
    capital = models.BooleanField("Capital")
    codigo_uf  = models.IntegerField('Código uf')