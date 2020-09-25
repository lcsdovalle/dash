# Generated by Django 2.2.9 on 2020-09-18 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0045_auto_20200918_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispersaoprofessor',
            name='maior_sessenta_dias',
            field=models.BigIntegerField(default=0, verbose_name='Maior que 60 dias'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dispersaoprofessor',
            name='sessenta_dias',
            field=models.BigIntegerField(default=0, verbose_name='Sessenta dias'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dispersaoprofessor',
            name='trinta_dias',
            field=models.BigIntegerField(default=0, verbose_name='Trinta dias'),
            preserve_default=False,
        ),
    ]