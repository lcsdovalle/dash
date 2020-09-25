# Generated by Django 2.2.9 on 2020-09-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0048_auto_20200924_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='NovoIuAluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('inep', models.CharField(max_length=100, verbose_name='Inep')),
                ('escola', models.CharField(max_length=100, verbose_name='Escola')),
                ('municipio', models.CharField(max_length=100, verbose_name='Município')),
                ('cre', models.CharField(max_length=100, verbose_name='Cre')),
                ('a_um_dia', models.IntegerField(verbose_name='Aluno cinco dias')),
                ('a_dois_dias', models.IntegerField(verbose_name='Aluno cinco dias')),
                ('a_tres_dias', models.IntegerField(verbose_name='Aluno cinco dias')),
                ('a_quatro_dias', models.IntegerField(verbose_name='Aluno cinco dias')),
                ('a_cinco_dias', models.IntegerField(verbose_name='Aluno cinco dias')),
                ('a_seis_dias', models.IntegerField(verbose_name='Aluno seois dias')),
                ('a_sete_dias', models.IntegerField(verbose_name='Aluno sete dias')),
                ('a_nenhum_dia', models.IntegerField(verbose_name='Aluno nenhum dia')),
            ],
        ),
    ]