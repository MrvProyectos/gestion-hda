from django.db import models

# Create your models here.

class Clientes(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50, verbose_name="Direcc. personal")
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")

    def __str__(self):

        return 'Nombre %s Direccion %s Email %s Telefono %s' % (self.nombre, self.direccion, self.email, self.telefono)

class Articulos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    seccion = models.CharField(max_length=20)
    precio = models.IntegerField()

class Pedidos(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField()
    estado = models.BooleanField(verbose_name="Entregado")
    pedango = models.CharField(max_length=4, verbose_name="Año")
    pedmes = models.CharField(max_length=2, verbose_name="Mes")

# Finantial Managment Home
# ========================

# Ingresos
class Fmhingreso(models.Model):
    ingango = models.CharField(max_length=4, verbose_name="Año")
    ingmes = models.CharField(max_length=2, verbose_name="Mes")
    ingcodtipo = models.CharField(max_length=5, verbose_name="Tipo de Ingreso")
    ingGlosa = models.CharField(max_length=70, verbose_name="Glosa")
    ingValor = models.IntegerField(verbose_name="Valor")

# Movimientos
class Fmhmovimiento(models.Model):
    movango = models.CharField(max_length=4, verbose_name="Año")
    movmes = models.CharField(max_length=2, verbose_name="Mes")
    movcodtipo = models.CharField(max_length=5, verbose_name="Tipo Mvto.")
    movglosa = models.CharField(max_length=70, verbose_name="Glosa Mvto.")
    movmto = models.IntegerField(verbose_name="Monto")
    movestado = models.BooleanField(verbose_name="Estado de Pago", default=0)

# Pagos
class Fmhpago(models.Model):
    pagango = models.CharField(max_length=4, verbose_name="Año")
    pagmes = models.CharField(max_length=2, verbose_name="Mes")
    pagidrefmov = models.IntegerField(verbose_name="Id Ref_Mov")
    pagfecha = models.DateField(verbose_name="Fecha de Pago")
    pagglosamov = models.CharField(max_length=70, verbose_name="Glosa Mvto.")
    pagtipdcto = models.CharField(max_length=3, verbose_name="Tipo Dcto. Pago")
    pagnumdocu = models.IntegerField(null=True, verbose_name="Num. Dcto.")
    pagmtomov = models.IntegerField(verbose_name="Mto. Movimiento")
    pagmtopago = models.PositiveIntegerField(verbose_name="Mto. Pago")
    pagestado = models.BooleanField(verbose_name="Estado de Pago")
    pagCodbco = models.CharField(null=True, max_length=3, verbose_name="Codigo Banco")
    pagMedpag = models.CharField(max_length=3, verbose_name="Medio Pago")
    pagNumchq = models.CharField(null=True, max_length=10, verbose_name="Nro. Cheque")
    
# Saldos
class Fmhsldenc(models.Model):
    sldango = models.CharField(max_length=4, verbose_name="Año")
    sldmes = models.CharField(max_length=2, verbose_name="Mes")
    sldingresos = models.IntegerField(verbose_name="Ingresos")
    sldegresos = models.IntegerField(verbose_name="Egresos")
    sldsaldo = models.IntegerField(verbose_name="Saldo")

# Detalle de Saldo
class Fmhslddet(models.Model):
    sdeango = models.CharField(max_length=4, verbose_name="Año")
    sdemes = models.CharField(max_length=2, verbose_name="Mes")
    sdecodsld = models.CharField(max_length=1, verbose_name="Cod. Saldo")
    sdeglosa = models.CharField(max_length=70, verbose_name="Glosa Detalle")
    sdeingresos = models.IntegerField(verbose_name="Ingresos")
    sdeegresos = models.IntegerField(verbose_name="Egresos")

# Periodos Procesados
class Fmhperproc(models.Model):
    procango = models.CharField(max_length=4, verbose_name="Año")
    procmes = models.CharField(max_length=2, verbose_name="Mes")

# Estadistica por tipo de gasto
class Fmhestadgasto(models.Model):
    estadango = models.CharField(max_length=4, verbose_name="Año")
    estadmes = models.CharField(max_length=2, verbose_name="Mes")
    estadgto1 = models.IntegerField(verbose_name="Financieros")
    estadgto2 = models.IntegerField(verbose_name="Fijos")
    estadgto3 = models.IntegerField(verbose_name="Autopistas")
    estadgto4 = models.IntegerField(verbose_name="Tecnología")
    estadgto5 = models.IntegerField(verbose_name="Gastos Médicos")
    estadgto6 = models.IntegerField(verbose_name="Colegios")
    estadgto7 = models.IntegerField(verbose_name="Supermercado")
    estadgto8 = models.IntegerField(verbose_name="Contribuciones")
    estadgto9 = models.IntegerField(verbose_name="Otros Gastos")

# Evolucion para grafico de pie
class Fmhevolgasto(models.Model):
    evolagno = models.CharField(max_length=4, verbose_name="Año")
    evolcepto1 = models.FloatField(verbose_name="Financieros")
    evolcepto2 = models.FloatField(verbose_name="Fijos")
    evolcepto3 = models.FloatField(verbose_name="Autopistas")
    evolcepto4 = models.FloatField(verbose_name="Tecnología")
    evolcepto5 = models.FloatField(verbose_name="Gastos Médicos")
    evolcepto6 = models.FloatField(verbose_name="Colegios")
    evolcepto7 = models.FloatField(verbose_name="Supermercado")
    evolcepto8 = models.FloatField(verbose_name="Contribuciones")
    evolcepto9 = models.FloatField(verbose_name="Otros Gastos")

# Aqui se guarda el ultimo periodo Procesado
class Fmhultperiodo(models.Model):
    ultango = models.CharField(max_length=4, verbose_name="Año")
    ultmes = models.CharField(max_length=2, verbose_name="Mes")
