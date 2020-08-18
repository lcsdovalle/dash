# Generated by Django 2.2.9 on 2020-08-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engajamento', '0008_atividade_turma_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraficoGeral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atividade_id', models.CharField(max_length=100, verbose_name='Atividade ID')),
                ('atividade_criacao', models.CharField(max_length=100, verbose_name='Atividade Criação')),
                ('atividade_atualizacao', models.CharField(max_length=100, verbose_name='Atividade Atualização')),
                ('escola_email', models.EmailField(max_length=254, verbose_name='Email Escola')),
                ('escola_nome', models.CharField(max_length=254, verbose_name='Nome escola')),
                ('escola_inep', models.IntegerField(verbose_name='Inep')),
                ('escola_cre', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cre')),
                ('municipio', models.CharField(max_length=254, verbose_name='Município')),
                ('regiao', models.CharField(max_length=254, verbose_name='Regiao')),
                ('turma_id', models.CharField(max_length=100, verbose_name='Turma id')),
                ('professor_nome', models.CharField(max_length=254, verbose_name='Professor nomee')),
                ('professor_email', models.EmailField(max_length=254, verbose_name='Professor email')),
                ('professor_id', models.CharField(max_length=100, verbose_name='Professor id')),
            ],
        ),
    ]
