# Generated by Django 2.2.9 on 2020-11-10 18:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0086_auto_20201110_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='data',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='data_publicacao',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Data'),
        ),
    ]
