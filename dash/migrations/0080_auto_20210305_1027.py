# Generated by Django 2.2.9 on 2021-03-05 13:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0079_auto_20201007_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcessosAlunos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('inep', models.CharField(blank=True, max_length=50, null=True, verbose_name='INEP')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('regiao', models.CharField(blank=True, max_length=200, null=True, verbose_name='Região')),
                ('municipio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Município')),
                ('cre', models.CharField(blank=True, max_length=100, null=True, verbose_name='CRE')),
            ],
        ),
        migrations.CreateModel(
            name='AcessosProfessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('inep', models.CharField(blank=True, max_length=50, null=True, verbose_name='INEP')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('regiao', models.CharField(blank=True, max_length=200, null=True, verbose_name='Região')),
                ('municipio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Município')),
                ('cre', models.CharField(blank=True, max_length=100, null=True, verbose_name='CRE')),
            ],
        ),
        migrations.DeleteModel(
            name='FuncaoDocente',
        ),
    ]