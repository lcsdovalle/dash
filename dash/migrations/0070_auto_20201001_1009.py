# Generated by Django 2.2.9 on 2020-10-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0069_auto_20200930_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='novaconsolidacaogeralaluno',
            name='ia',
            field=models.BigIntegerField(default=0, verbose_name='Ia'),
        ),
        migrations.AddField(
            model_name='novaconsolidacaogeralaluno',
            name='ie',
            field=models.BigIntegerField(default=0, verbose_name='Ie'),
        ),
        migrations.AddField(
            model_name='novaconsolidacaogeralaluno',
            name='iu',
            field=models.BigIntegerField(default=0, verbose_name='Iu'),
        ),
    ]
