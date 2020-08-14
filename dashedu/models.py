# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.
class InteracoesClassroomPorTipoUsuario(models.Model):
    data = models.DateField('Quando', auto_now=False, auto_now_add=False)
    professores = models.IntegerField('Professores')
    alunos = models.IntegerField('Alunos')
    turmas_criadas = models.IntegerField('Número de turmas criadas',default=0)
    alunos_posts_criados = models.IntegerField('Número de posts criados por alunos',default=0)
    professores_posts_criados = models.IntegerField('Número de posts criados por professores',default=0)
    outros = models.IntegerField('Outros',null=True,blank=True)

    def __str__(self):
        return 'Relatório do dia {}'.format(self.data.strftime('%d/%m/%Y'))

class RelatorioUsuarios(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    name = models.CharField('Nome', max_length=255)
    uso_drive = models.IntegerField('Uso do Drive')
    ultimo_acesso = models.CharField('Último acesso', max_length=100)
    turmas_criadas = models.IntegerField('Turmas criadas')
    posts_criados = models.IntegerField('Posts criados')
    papel = models.CharField('Papel', max_length=50,choices=(('teacher','Professor'),('student','Aluno')))
    ultimo_acesso_classroom = models.CharField('Último acesso classroom', max_length=100)
    codigo_usuario = models.IntegerField('Código usuário')
    regiao = models.CharField('Região', max_length=200)
    municipio = models.CharField('Município', max_length=200)
    inep = models.IntegerField('INEP')
    codigo_escola = models.IntegerField('Código Escola')
    nome_escola = models.CharField('Nome Escola', max_length=254)
class TotalTurmas(models.Model):
    total = models.IntegerField('Total')
    
    def __str__(self):
        return str(self.total)
    
class TotalUsuarios(models.Model):
    total = models.IntegerField('Total')

    def __str__(self):
        return str(self.total)

class UsoChromebooks(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    quantidade = models.IntegerField('quantidade')

class EventosClassrom(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    quantidade_estudantes = models.IntegerField('Quantidade Estudantes')
    quantidade_estudantes = models.IntegerField('Quantidade Professores')
    turmas_criadas = models.IntegerField('Quantidade Interações')
    posts_criados = models.IntegerField('Quantidade Pots Criados')
    def __str__(self):
        return 'Relatório do dia {}'.format(self.data.strftime('%d/%m/%Y'))
    

class EventosDrive(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    comentarios = models.IntegerField('Comentários')
    visualizacoes = models.IntegerField('Visualizações')
    criacao_arquivos = models.IntegerField('Arquivos criados')
    compartilhamentos = models.IntegerField('Arquivos compartilhados')

    def __str__(self):
        return 'Relatório do dia {}'.format(self.data.strftime('%d/%m/%Y'))
class Logins(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    logins = models.IntegerField('Quantidade')

