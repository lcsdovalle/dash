# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Escola,Turmas,Atividade,Professor,Aluno
from django.contrib import admin

admin.site.register(Escola)
admin.site.register(Turmas)
admin.site.register(Atividade)
admin.site.register(Professor)
admin.site.register(Aluno)

# Register your models here.
