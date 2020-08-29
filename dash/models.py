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
    data = models.DateField('Data', auto_now_add=True)
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    total = models.IntegerField('Total')
    acessaram = models.IntegerField('Acessaram')

    class Meta:
        verbose_name = ("IA Aluno")
        verbose_name_plural = ("IA Alunos")

    def __str_(self):
        return self.nome

class IaIndicadorProfessor(models.Model):
    data = models.DateField('Data', auto_now_add=True)
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)    
    regiao = models.CharField('Região', max_length=200,blank=True,null=True)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    total = models.IntegerField('Total')
    acessaram = models.IntegerField('Acessaram')

    class Meta:
        verbose_name = ("IA Aluno")
        verbose_name_plural = ("IA Alunos")

    def __str_(self):
        return self.nome