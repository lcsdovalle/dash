# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.
class InteracoesClassroomPorTipoUsuario(models.Model):
    data = models.DateField('Quando', auto_now=False, auto_now_add=False)
    professores = models.BigIntegerField('Professores')
    alunos = models.BigIntegerField('Alunos')
    turmas_criadas = models.BigIntegerField('Número de turmas criadas',default=0)
    alunos_posts_criados = models.BigIntegerField('Número de posts criados por alunos',default=0)
    professores_posts_criados = models.BigIntegerField('Número de posts criados por professores',default=0)
    outros = models.BigIntegerField('Outros',null=True,blank=True)

    def __str__(self):
        return 'Relatório do dia {}'.format(self.data.strftime('%d/%m/%Y'))

class RelatorioUsuarios(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    name = models.CharField('Nome', max_length=255)
    uso_drive = models.BigIntegerField('Uso do Drive')
    ultimo_acesso = models.CharField('Último acesso', max_length=100)
    turmas_criadas = models.BigIntegerField('Turmas criadas')
    posts_criados = models.BigIntegerField('Posts criados')
    papel = models.CharField('Papel', max_length=50,choices=(('Professor','Professor'),('Aluno','Aluno')))
    ultimo_acesso_classroom = models.CharField('Último acesso classroom', max_length=100)
    codigo_usuario = models.BigIntegerField('Código usuário')
    regiao = models.CharField('Região', max_length=200)
    municipio = models.CharField('Município', max_length=200)
    inep = models.BigIntegerField('INEP')
    codigo_escola = models.BigIntegerField('Código Escola')
    nome_escola = models.CharField('Nome Escola', max_length=254)
class TotalTurmas(models.Model):
    total = models.BigIntegerField('Total')
    
    def __str__(self):
        return str(self.total)
    
class TotalUsuarios(models.Model):
    total = models.BigIntegerField('Total')

    def __str__(self):
        return str(self.total)

class UsoChromebooks(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    quantidade = models.BigIntegerField('quantidade')

class EventosClassrom(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    quantidade_estudantes = models.BigIntegerField('Quantidade Estudantes')
    quantidade_estudantes = models.BigIntegerField('Quantidade Professores')
    turmas_criadas = models.BigIntegerField('Quantidade Interações')
    posts_criados = models.BigIntegerField('Quantidade Pots Criados')
    def __str__(self):
        return 'Relatório do dia {}'.format(self.data.strftime('%d/%m/%Y'))
    

class EventosDrive(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    comentarios = models.BigIntegerField('Comentários')
    visualizacoes = models.BigIntegerField('Visualizações')
    criacao_arquivos = models.BigIntegerField('Arquivos criados')
    compartilhamentos = models.BigIntegerField('Arquivos compartilhados')

    def __str__(self):
        return 'Relatório do dia {}'.format(self.data.strftime('%d/%m/%Y'))
class Logins(models.Model):
    data = models.DateField('Data', auto_now=False, auto_now_add=False)
    logins = models.BigIntegerField('Quantidade')

