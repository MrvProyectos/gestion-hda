# Generated by Django 3.0.6 on 2020-06-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0012_auto_20200619_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fmhpago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagango', models.CharField(max_length=4, verbose_name='Año')),
                ('pagmes', models.CharField(max_length=2, verbose_name='Mes')),
                ('pagidrefmov', models.IntegerField(verbose_name='Id Ref_Mov')),
                ('pagfecha', models.DateField(verbose_name='Fecha de Pago')),
                ('pagglosamov', models.CharField(max_length=70, verbose_name='Glosa Mvto.')),
                ('pagtipdcto', models.CharField(max_length=3, verbose_name='Tipo Dcto. Pago')),
                ('pagnumdocu', models.IntegerField(verbose_name='Num. Dcto.')),
                ('pagmtomov', models.IntegerField(verbose_name='Mto. Movimiento')),
                ('pagmtopago', models.IntegerField(verbose_name='Mto. Pago')),
                ('pagestado', models.BooleanField(verbose_name='Estado de Pago')),
            ],
        ),
        migrations.AddField(
            model_name='fmhmovimiento',
            name='movestado',
            field=models.BooleanField(default=0, verbose_name='Estado de Pago'),
        ),
    ]