# Generated by Django 3.0.6 on 2020-05-21 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0003_auto_20200520_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidos',
            name='estado',
            field=models.BooleanField(verbose_name='Entregado'),
        ),
    ]
