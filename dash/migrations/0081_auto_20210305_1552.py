# Generated by Django 2.2.9 on 2021-03-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0080_auto_20210305_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acessosalunos',
            name='inep',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='INEP'),
        ),
        migrations.AlterField(
            model_name='acessosprofessor',
            name='inep',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='INEP'),
        ),
    ]