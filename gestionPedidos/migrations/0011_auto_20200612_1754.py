# Generated by Django 3.0.6 on 2020-06-12 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0010_auto_20200604_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='pedango',
            field=models.CharField(default='2020', max_length=4, verbose_name='Año'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='pedmes',
            field=models.CharField(default='01', max_length=2, verbose_name='Mes'),
        ),
    ]