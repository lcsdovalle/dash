# Generated by Django 2.2.9 on 2020-09-28 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0058_novocadastroatividades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novocadastroatividades',
            name='componente_curricular',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Componente curricular'),
        ),
    ]
