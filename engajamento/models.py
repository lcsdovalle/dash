# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Create your models here.
class Turmas(models.Model):
    name = models.CharField("Name", max_length=255,null=True,blank=True)
    turma_id = models.CharField("id", max_length=100,unique=True)
    owner_id = models.CharField('Owner', max_length=100)    
    section = models.CharField('Section', max_length=255,null=True,blank=True)
    owner_email = models.EmailField('Email')
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

    def __str_(self):
        return self.name

class Atividade(models.Model):
    title = models.CharField('Title', max_length=100,null=True,blank=True)
    atividade_id = models.CharField('ID', max_length=200,unique=True)
    due = models.DateTimeField('Due', auto_now=False, auto_now_add=False,null=True,blank=True)
    state = models.CharField('Course State', max_length=50)
    creator_id = models.CharField('Creator', max_length=100)
    criado = models.CharField('Data criação', max_length=100)
    atualizado = models.CharField('Data atualização', max_length=100)
    turma_id = models.CharField('ID', max_length=200,default='00000')

    class Meta:
        verbose_name = ("Atividade")
        verbose_name_plural = ("Atividades")

    def __str_(self):
        return self.title

class Professor(models.Model):
    nome = models.CharField('Name', max_length=255)
    email = models.EmailField('Email', max_length=254,unique=True)
    professor_id = models.CharField('Id', max_length=200,unique=True)
    matricula = models.CharField('Matricula', max_length=50,null=True,blank=False)
    cpf = models.CharField('Cpf', max_length=50,null=True,blank=False)
    ultimo_acesso = models.CharField('Ultimo acesso', max_length=100)

    class Meta:
        verbose_name = ("Professor")
        verbose_name_plural = ("Professores")

    def __str_(self):
        return self.name

class Aluno(models.Model):
    name = models.CharField('Name', max_length=255)
    email = models.EmailField('Email', max_length=254,unique=True)
    aluno_id = models.CharField('Id', max_length=200,unique=True)    
    matricula = models.CharField('Matricula', max_length=50,null=True,blank=False)
    cpf = models.CharField('Cpf', max_length=50,null=True,blank=False)

    class Meta:
        verbose_name = ("Aluno")
        verbose_name_plural = ("Alunos")

    def __str_(self):
        return self.name


class Escola(models.Model):
    nome = models.CharField('Nome', max_length=255)
    inep = models.CharField('INEP', max_length=50)
    email = models.EmailField('Email', max_length=254,blank=True,null=True,unique=True)
    regiao = models.CharField('Região', max_length=200)
    municipio = models.CharField('Município', max_length=50)
    cre = models.CharField('CRE', max_length=100,blank=True,null=True)
    class Meta:
        verbose_name = ("Escola")
        verbose_name_plural = ("Escolas")

    def __str_(self):
        return self.nome




