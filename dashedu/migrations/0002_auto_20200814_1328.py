# Generated by Django 2.2.9 on 2020-08-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashedu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interacoesclassroomportipousuario',
            name='outros',
            field=models.IntegerField(blank=True, null=True, verbose_name='Outros'),
        ),
    ]