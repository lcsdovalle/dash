# Generated by Django 2.2.9 on 2020-11-10 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0085_ultimostatusprofessor_lat_lon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='criador',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Criador'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='inep',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='INEP'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='municipio',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Município'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='qtd_atrasos',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Atrasos'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='qtd_corrigida',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Corrigidas'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='qtd_iniciada',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Iniciada'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='qtd_nao_iniciada',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Não iniciada'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='qtd_vinculos',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Vínculos'),
        ),
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='turma_id',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Turma'),
        ),
    ]
