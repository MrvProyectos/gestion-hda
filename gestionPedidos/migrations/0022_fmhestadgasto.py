# Generated by Django 3.0.6 on 2020-07-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0021_auto_20200709_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fmhestadgasto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estadango', models.CharField(max_length=4, verbose_name='Año')),
                ('estadmes', models.CharField(max_length=2, verbose_name='Mes')),
                ('estadgto1', models.IntegerField(verbose_name='Financieros')),
                ('estadgto2', models.IntegerField(verbose_name='Fijos')),
                ('estadgto3', models.IntegerField(verbose_name='Autopistas')),
                ('estadgto4', models.IntegerField(verbose_name='Tecnología')),
                ('estadgto5', models.IntegerField(verbose_name='Gastos Médicos')),
                ('estadgto6', models.IntegerField(verbose_name='Colegios')),
                ('estadgto7', models.IntegerField(verbose_name='Supermercado')),
                ('estadgto8', models.IntegerField(verbose_name='Contribuciones')),
                ('estadgto9', models.IntegerField(verbose_name='Otros Gastos')),
            ],
        ),
    ]
