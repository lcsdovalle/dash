# Generated by Django 2.2.9 on 2020-11-09 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0082_auto_20201109_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acessosalunos',
            name='inep',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='INEP'),
        ),
        migrations.AlterField(
            model_name='acessosalunos',
            name='municipio',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Município'),
        ),
    ]
