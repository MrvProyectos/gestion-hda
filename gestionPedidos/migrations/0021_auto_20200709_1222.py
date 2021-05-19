# Generated by Django 3.0.6 on 2020-07-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0020_auto_20200705_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fmhperproc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procango', models.CharField(max_length=4, verbose_name='Año')),
                ('procmes', models.CharField(max_length=2, verbose_name='Mes')),
            ],
        ),
        migrations.AlterField(
            model_name='fmhpago',
            name='pagMedpag',
            field=models.CharField(max_length=3, verbose_name='Medio Pago'),
        ),
        migrations.AlterField(
            model_name='fmhpago',
            name='pagNumchq',
            field=models.CharField(max_length=10, null=True, verbose_name='Nro. Cheque'),
        ),
    ]
