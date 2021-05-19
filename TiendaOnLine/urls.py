"""TiendaOnLine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# Proyecto
from gestionPedidos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('busqueda_productos/', views.busqueda_productos, name='buscaProd'),
    path('listaArticulos/', views.listarArticulos, name='listadoArt'),
    path('buscarElProd/', views.buscarElProd),
    path('contacto/', views.contacto),
    path('creaClientes/', views.creaClientes, name='creacionClte'),
    path('creaClientesBD/', views.creaClientesBD),
    path('eliminar/<int:id>', views.eliminarArticulos, name='eliminar_id'),
    path('actArticulos/<int:id_art>', views.actArticulos, name='actualizaArt_id'),
    path('listado_de_clientes/', views.ListaClientes, name='listaClte'),
    # ================
    # Proyecyo Gestion
    # ================
    # Inicio de Session
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #
    path('mensajeSistema/<int:pcodMsg>/<str:ptipMsg>', views.fmhMsgSistema, name='msgSistema'),
    path('Gestion_Hogar/', views.fmh_Gestion, name="gestionHogar"),
    # Ingresos
    path('Ingresos/', views.fmhIngresosHab, name="IngresoHab"),
    # Ingreso de Movimientos
    path('IngresoMov/', views.fmhIngresoMvtos, name='IngresoDeb'),
    path('ListaMvtos/', views.fmhListaMov, name='listaMvtos'),
    # Listado Gestion de Ingreso
    path('GestionarIngreso/', views.fmhGestionIngreso, name='gestionIngreso'),
    path('EliminaIngreso/<int:pId>/<int:pAngo>/<int:pMes>', views.fmhEliminaId, name='eliminaIng'),
    path('EliminarBDIng/<int:pId>', views.eliminarBDIng, name='eliminarBDIng'),
    # Vistas para gestionar ingresos
    path('formActIng/<int:pId>', views.fmhActualizaIng, name='actualizaIng'),
    path('ElimselallIng/', views.ElimselallIng),
    # Vistas para gestionar movimientos
    path('GestionarMvtos/<int:pEstado>', views.fmhGestionMvtos, name='gestionMovimientos'),
    path('EliminaMvto/<int:pId>/<int:pAngo>/<int:pMes>', views.fmhEliminaIdmov, name='eliminaMov'),
    path('EliminarBDMov/<int:pId>', views.eliminarBDMov, name='eliminarBDMov'),
    path('ElimselallMov/', views.ElimselallMov),
    path('formActMov/<int:pId>', views.fmhActualizaMov, name='actualizaMov'),
    # Pagos
    path('listadoPagosPend', views.fmhListPagPen, name='listaPagPend'),
    path('pagoDcto/<int:pId>/<int:pIdref>', views.fmhPagoDcto, name='pagoDocumento'),
    path('vueltaMov/', views.vuelveGestionMov, name='vuelveGMovimie'),
    path('fmhPosponerPago/', views.fmhPosponerPago),
    # Saldos
    path('fmhSaldosPeriodo/', views.fmhSaldosPeriodo),
    #Eliminar saldos
    path('saldos/<int:parango>/<int:parmes>', views.fmhSaldos, name='consultasaldos'),
    #========
    # Vuelve al template Anterior
    path('vueltaIng/', views.vuelveGestionIng, name='vuelveGIngreso'),
    # Copia periodo
    path('fmhreplica/', views.fmhreplica),
    path('replicaPeriodo/<int:newpango>/<int:newpmes>', views.fmhCopiaMovPag, name='replicaPeriodo'),
    # Cierre del Proceso
    path('cierreProceso/', views.fmhcierreProc, name='cierreProc'),
    #Estadisticas
    path('estadistica/', views.fmhObtieneSaldos, name='estadistica'),
    path('estadGastos/', views.fmhEstadGastos, name='estadGastos'),
    # Session Periodo
    path('fmhCreasession/', views.fmhCreasession),
    path('fmhSuspendeSess/', views.fmhsuspendeSess, name='suspendeSesion'),
    # Consulta General
    path('fmhConsGral/', views.fmhConsGral),
    path('consulta_general/<int:parango>/<str:parmes>', views.fmhConsultaGral, name='consulta_gral'),
]