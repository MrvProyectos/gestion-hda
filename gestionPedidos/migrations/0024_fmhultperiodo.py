# Generated by Django 3.0.6 on 2021-03-06 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0023_fmhevolgasto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fmhultperiodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ultango', models.CharField(max_length=4, verbose_name='Año')),
                ('ultmes', models.CharField(max_length=2, verbose_name='Mes')),
            ],
        ),
    ]
