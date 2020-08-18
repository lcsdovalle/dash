# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Escola,Turmas,Atividade,Professor,Aluno,GraficoAuxiliar,GraficoEngajamento
from django.contrib import admin

admin.site.register(Escola)
admin.site.register(Turmas)
admin.site.register(Atividade)
admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(GraficoAuxiliar)

@admin.register(GraficoEngajamento)
class GraficoEngajamentoAdmin(admin.ModelAdmin):
    list_display = ('inep',)
    search_fields = ('inep',)

# Register your models here.
