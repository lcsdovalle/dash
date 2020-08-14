# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.
class InteracoesClassroomPorTipoUsuario(models.Model):
    data = models.DateField('Quando', auto_now=False, auto_now_add=False)
    professores = models.IntegerField('Professores')
    alunos = models.IntegerField('Alunos')
    outros = models.IntegerField('Outros')

    def __str__(self):
        return self.data

class TotalTurmas(models.Model):
    total = models.IntegerField('Total')
    
    def __str__(self):
        return self.total
    
class TotalUsuarios(models.Model):
    total = models.IntegerField('Total')

    def __str__(self):
        return self.total

class UsoChromebooks(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    quantidade = models.IntegerField('quantidade')

class EventosClassrom(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    quantidade_estudantes = models.IntegerField('Quantidade Estudantes')
    quantidade_estudantes = models.IntegerField('Quantidade Professores')
    turmas_criadas = models.IntegerField('Quantidade Interações')
    posts_criados = models.IntegerField('Quantidade Pots Criados')

class EventosDrive(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    comentarios = models.IntegerField('Comentários')
    visualizacoes = models.IntegerField('Visualizações')
    criacao_arquivos = models.IntegerField('Arquivos criados')
    compartilhamentos = models.IntegerField('Arquivos compartilhados')

    def __str__(self):
        return self.data
class Logins(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    logins = models.IntegerField('Quantidade')

class RelatorioUsuario(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    turmas_criadas = models.IntegerField('Turmas Criadas')
    arquivos_criados = models.IntegerField('Arquivos Criados')
    posts_criados = models.IntegerField('Pots Criados')
    papel = models.CharField('Papel', max_length=50, choices=(('teacher','Professor'),('student','Aluno')))
    ultima_interacao = models.DateTimeField('Quando', auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.data
    