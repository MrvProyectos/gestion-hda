from django.contrib import admin
from gestionPedidos.models import Clientes, Articulos, Pedidos, Fmhingreso, Fmhmovimiento, Fmhpago, \
                                  Fmhsldenc, Fmhslddet, Fmhperproc, Fmhestadgasto, Fmhevolgasto

# Register your models here.

# Clase que permite ver en el panel de administracion la informacion como tabla.
class ClientesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "email", "telefono")
    # Busqueda de Clientes
    search_fields = ("nombre", "telefono")

class ArticulosAdmin(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("nombre", "seccion", "precio")
    # Busqueda
    search_fields = ("nombre",)
    # Filtro
    list_filter = ("seccion",)

class PedidosAdmin(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("pedango", "pedmes", "numero", "fecha", "estado")
    # Filtro tipo Fecha
    list_filter=("fecha",)
    # Filtro Fecha Tipo Menu
    date_hierarchy="fecha"

# FIMAHO
# ======

# Ingresos
class IngresosAdmin(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("ingango", "ingmes", "ingcodtipo", "ingGlosa", "ingValor")
    # filtros
    list_filter=("ingango", "ingmes",)

# Movimientos
class MovimientosAdmin(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("movango", "movmes", "movcodtipo", "movglosa", "movmto", "movestado")
    # filtros
    list_filter = ("movango", "movmes", "movestado",)

# Pagos
class PagosAdmin(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("pagango", "pagmes", "pagidrefmov", "pagfecha", "pagglosamov", "pagtipdcto", "pagnumdocu", "pagmtomov", "pagmtopago", "pagestado", "pagCodbco")
    # Filtros
    list_filter = ("pagango", "pagmes",)

# Saldos Encabezado
class Saldosenc(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("sldango", "sldmes", "sldingresos", "sldegresos", "sldsaldo")
    # Filtros
    list_filter = ("sldango", "sldmes",)

# Saldos Detalle
class Saldosdet(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("sdeango", "sdemes", "sdecodsld", "sdeglosa", "sdeingresos", "sdeegresos")
    # Filtros
    list_filter = ("sdeango", "sdemes",)

# Periodos Procesados
class PeriodosProc(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("procango", "procmes")
    # Filtros
    list_filter = ("procango", "procmes",)

# Estadistica por Tipo de Gasto
class EstadisticaGasto(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("estadango", "estadmes", "estadgto1", "estadgto2", "estadgto3", "estadgto4", "estadgto5", "estadgto6", "estadgto7", "estadgto8", "estadgto9")
    # Filtros
    list_filter = ("estadango", "estadmes",)

# Evolucion de gastos para grafico de Pie
class EvolucionGastos(admin.ModelAdmin):
    # Modo Tabla
    list_display = ("evolagno", "evolcepto1", "evolcepto2", "evolcepto3", "evolcepto4", "evolcepto5", "evolcepto6", "evolcepto7", "evolcepto8", "evolcepto9")
    # Filtros
    list_filter = ("evolagno",)

# Registrando
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(Pedidos, PedidosAdmin)
admin.site.register(Fmhingreso, IngresosAdmin)
admin.site.register(Fmhmovimiento, MovimientosAdmin)
admin.site.register(Fmhpago, PagosAdmin)
admin.site.register(Fmhsldenc, Saldosenc)
admin.site.register(Fmhslddet, Saldosdet)
admin.site.register(Fmhperproc, PeriodosProc)
admin.site.register(Fmhestadgasto, EstadisticaGasto)
admin.site.register(Fmhevolgasto, EvolucionGastos)