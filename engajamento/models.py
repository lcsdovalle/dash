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

    class Meta:
        verbose_name = ("Professor")
        verbose_name_plural = ("Professores")

    def __str_(self):
        return self.nome

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


class GraficoGeral(models.Model):
    atividade_id = models.CharField('Atividade ID', max_length=100)
    atividade_criacao = models.CharField('Atividade Criação', max_length=100)
    atividade_atualizacao = models.CharField('Atividade Atualização', max_length=100)

    escola_email = models.EmailField('Email Escola')
    escola_nome = models.CharField('Nome escola', max_length=254)
    escola_inep = models.IntegerField('Inep')
    escola_cre = models.CharField('Cre', max_length=50,null=True,blank=True)
    
    municipio = models.CharField('Município', max_length=254)
    regiao = models.CharField('Regiao', max_length=254)
    
    turma_id = models.CharField('Turma id', max_length=100)
    
    professor_nome = models.CharField('Professor nomee', max_length=254)
    professor_email = models.EmailField('Professor email')
    professor_id = models.CharField('Professor id', max_length=100)

    def __str__(self):
        return "{} | {} | {} ".format(
            self.professor_nome,
            self.escola_nome,
            self.atividade_id
        )