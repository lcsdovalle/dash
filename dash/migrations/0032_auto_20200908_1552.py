# Generated by Django 2.2.9 on 2020-09-08 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0031_auto_20200908_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='cpf',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Cpf'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='inep',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Inep'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='matricula',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Matricula'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='nome',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='status',
            field=models.IntegerField(blank=True, null=True, verbose_name='Status'),
        ),
    ]
