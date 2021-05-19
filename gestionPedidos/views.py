
# Estadistica
import json
#
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Max, Q
from django.db import models
from datetime import datetime

from gestionPedidos.models import Articulos, Clientes, Fmhingreso, Fmhmovimiento, Fmhpago, Fmhsldenc, Fmhslddet, \
                                  Fmhperproc, Fmhestadgasto, Fmhevolgasto, Fmhultperiodo

from gestionPedidos.forms import FormularioContacto, ArticulosForm, Formacting, Formmvtos, Formpagos, FormSldPeriodo, \
                                    FormIngreso, FormIngmvtos


# Create your views here.
def busqueda_productos(request):
    return render(request, "busqueda_productos.html")

def listarArticulos(request):    
    listado = Articulos.objects.all()
    contextoListado = {'listado':listado}
    return render(request, 'resultados_listado.html', contextoListado)

def buscarElProd(request):
    
    if request.GET["prd"]:
        #mensaje="El producto buscado: %r" %request.GET["prd"]
        producto = request.GET["prd"]

        if len(producto)>20:
            mensaje="El texto de la busqueda es demaciado extenso"
        else:
            artBuscado=Articulos.objects.filter(seccion__icontains=producto).order_by('id')
            return render(request, "resultados_busqueda.html", {"articulos":artBuscado, "query":producto})
    else:
        mensaje="Producto invalido"

    return HttpResponse(mensaje)

# Funcion de contacto para formulario
def contacto(request):

    if request.method=="POST":

        miFormulario=FormularioContacto(request.POST)

        if miFormulario.is_valid():
            infForm=miFormulario.cleaned_data

            return render(request, "gracias.html")

    else:
        miFormulario=FormularioContacto()

    return render(request, "formulario_contacto.html", {"form":miFormulario})

def creaClientes(request):
    return render(request, "creaClientes.html")

def creaClientesBD(request):

    if request.method=="POST":
        clteNombre=request.POST["nombre"]
        clteDirecc=request.POST["direccion"]
        clteEmail=request.POST["email"]
        clteTelfon=request.POST["telefono"]
        
        # Metodo 1
        #clientesNuevos=Clientes(nombre=clteNombre, direccion=clteDirecc, email=clteEmail, telefono=clteTelfon)
        #clientesNuevos.save()

        # Metodo 2
        clientesNuevos=Clientes.objects.create(nombre=clteNombre, direccion=clteDirecc, email=clteEmail, telefono=clteTelfon)
        return redirect('listaClte')
        #return redirect('creacionClte')
        
    else:
        mensaje="Formulario Invalido"

    return HttpResponse(mensaje)

def eliminarArticulos(request, id):
    registroElim=Articulos.objects.get(id=id)
    registroElim.delete()

    return redirect('listadoArt')

def actArticulos(request, id_art):

    # Valor a pasar al html
    idArticulo=id_art
    # Instancia
    articulos = Articulos.objects.get(id=id_art)

    if request.method == "POST":
        # Actualizar el formulario 
        form = ArticulosForm(request.POST, instance=articulos)
        if form.is_valid():
            form.save()

        return redirect('listadoArt')
    else:
        # Creamos el formulario
        form = ArticulosForm(instance=articulos)

    return render(request, 'actualizaArticulos.html', {"id_Articulo":idArticulo, 'form': form})

# Ejecutar Procedimientos directamente desde la base de datos MySql
def ListaClientes(request):

    pvalor ="10"

    # Importamos conexion
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.callproc('prcListaClientes', {pvalor})
        #cursor.callproc('prcCierremensual', {pvalor})
       
        resultData = cursor.fetchall()

        resultLista=[]

        for row in resultData:
            resultLista.append(list(row))

        contexto = {'consultas':resultLista}

    return render(request, 'listaClientes.html', contexto)

# ===========================
# Proyecto Gestion Financiera
# ===========================

# Definicion de Funciones
# =======================

# Devuelve en modo texto año y mes de proceso
def fncDevuelvemes(pperiodo):
    pango = pperiodo[0:4]
    pmes = pperiodo[-2:]

    if pmes=='01':
        descripcion ='Enero'
    elif pmes=='02':
        descripcion ='Febrero'
    elif pmes=='03':
        descripcion ='Marzo'
    elif pmes=='04':
        descripcion ='Abril'
    elif pmes=='05':
        descripcion ='Mayo'
    elif pmes=='06':
        descripcion ='Junio'
    elif pmes=='07':
        descripcion ='Julio'
    elif pmes=='08':
        descripcion ='Agosto'
    elif pmes=='09':
        descripcion ='Septiembre'
    elif pmes=='10':
        descripcion ='Octubre'
    elif pmes=='11':
        descripcion ='Noviembre'
    elif pmes=='12':
        descripcion ='Diciembre'
    else:
        descripcion ='---------'

    descContexto = pango + " - " + descripcion
    return descContexto

# Funcion que devuelve el mes en formato string
def fncMes(pMes):
    if pMes==1:
        varMes ="01"
    elif pMes==2:
        varMes ="02"
    elif pMes==3:
        varMes ="03"
    elif pMes==4:
        varMes ="04"
    elif pMes==5:
        varMes ="05"
    elif pMes==6:
        varMes ="06"
    elif pMes==7:
        varMes ="07"
    elif pMes==8:
        varMes ="08"
    elif pMes==9:
        varMes ="09"
    else:
        varMes =pMes

    return varMes

# Devuelve nombre del mes
def fncNomMes(pmes):
    if pmes=='01':
        descripcion ='Enero'
    elif pmes=='02':
        descripcion ='Febrero'
    elif pmes=='03':
        descripcion ='Marzo'
    elif pmes=='04':
        descripcion ='Abril'
    elif pmes=='05':
        descripcion ='Mayo'
    elif pmes=='06':
        descripcion ='Junio'
    elif pmes=='07':
        descripcion ='Julio'
    elif pmes=='08':
        descripcion ='Agosto'
    elif pmes=='09':
        descripcion ='Septiembre'
    elif pmes=='10':
        descripcion ='Octubre'
    elif pmes=='11':
        descripcion ='Noviembre'
    elif pmes=='12':
        descripcion ='Diciembre'
    else:
        descripcion ='---------'

    return descripcion

# Funcion Recupera Session
def fncSession(request):
    if "periodo" in request.session:
        cadenaFecha = request.session.get('periodo')
    else:
        cadenaFecha='000000'
    return cadenaFecha

# Funcion que elimina registros Pagos
def fncElimPagos(parId):

    try:
        regPagos = Fmhpago.objects.get(pagidrefmov=parId)
        regPagos.delete()
    except:
        var=0

# Funcion que actualiza monto pago
def fncActualizaPagos(parId, pconcepto, parMonto):

    # Actualizar Monto Pago 
    from django.db import connection
    with connection.cursor() as pag:

        try:
            pag.execute("update hdagestion.gestionpedidos_fmhpago set pagmtomov =%s, pagglosamov=%s" \
                " where pagidrefmov = %s", [parMonto, pconcepto, parId])
        except:
            var=0

# Funcion para copiar el ultimo periodo cerrado.
def fncCopiaPeriodo(pAngoNew, pMesNew, pAngoCopia, pMesCopia, pEstado):
    # Conecta BD
    from django.db import connection
    with  connection.cursor() as insmp:

        pMesNew =fncMes(pMesNew)
        pMesCopia = fncMes(pMesCopia)

        # Movimientos
        try:
            insmp.execute("insert into hdagestion.gestionpedidos_fmhmovimiento(movango, movmes, movcodtipo, movglosa, movmto, movestado)" \
                " select %s, %s, movcodtipo, movglosa, movmto, %s from hdagestion.gestionpedidos_fmhmovimiento where movango=%s and movmes=%s" \
                    ,[pAngoNew, pMesNew, pEstado, pAngoCopia, pMesCopia])
        except:
            documento = """
            <html>
            <body>
            <h1> Error en la Copia Movimientos</h1>
            </body>
            </html>
            """
            return HttpResponse(documento)

        # Pagos
        vfechaActual = datetime.now()
        vtipodcto = '000'
        vmediopago = '000'

        try:
            insmp.execute("insert into hdagestion.gestionpedidos_fmhpago(pagango, pagmes, pagidrefmov, pagfecha, pagglosamov, pagtipdcto, pagmtomov, pagmtopago, pagestado, pagMedpag)" \
                " select %s, %s, id, %s, movglosa, %s, movmto, 0, %s, %s from hdagestion.gestionpedidos_fmhmovimiento where movango=%s and movmes=%s" \
                    ,[pAngoNew, pMesNew, vfechaActual, vtipodcto, pEstado, vmediopago, pAngoNew, pMesNew])

        except:
            documento = """
            <html>
            <body>
            <h1> Error en la Copia Pagos</h1>
            </body>
            </html>
            """
            return HttpResponse(documento)

# Valida Periodos Procesados
def fncValPerProc(pAngo, pMes):
    
    resultQS = Fmhperproc.objects.filter(procango__icontains=pAngo, procmes__icontains=pMes)
    resultado = resultQS.values()
    
    if resultado:
        return True
    else:
        return False

# Funcion trae ultimo periodo
def fncUltimoPer():
    # Rescata Ultimo Periodo Cerrado
    ultreg = Fmhultperiodo.objects.all().aggregate(maxAngo=Max('ultango'),
                                                   maxMes=Max('ultmes')
                                                )

    if ultreg:
        angoUlt = ultreg.get('maxAngo')
        mesUlt = ultreg.get('maxMes')
    else:
        angoUlt = 'X'
        mesUlt = 'X'

    return (angoUlt, mesUlt)

# ======
# Vistas
# ======

# Mensaje de Stop o Warning generado por Sistema
def fmhMsgSistema(request, pcodMsg, ptipMsg):
    msgTitulo ='SISTEMA DE MENSAJERIA'
    msgSistema =''

    # Definicion de mensaje de Error o Advertencia
    if   pcodMsg ==1:   msgSistema ='Se debe inicializar un período para continuar...'
    elif pcodMsg ==2:   msgSistema ='No existe un periodo inicializado para cerrar proceso...'
    elif pcodMsg ==3:   msgSistema ='Este período ya realizó CIERRE DE PROCESO...'
    elif pcodMsg ==4:   msgSistema ='No se han seleccionado registros para Eliminar...'
    elif pcodMsg ==5:   msgSistema ='El nuevo período ya tiene Movimientos generados...'
    elif pcodMsg ==6:   msgSistema ='Período se encuentra CERRADO...'
    elif pcodMsg ==7:   msgSistema ='Sesion Suspendida con Exito...'
    elif pcodMsg ==8:   msgSistema ='Proceso de cierre generado con Exito...'
    elif pcodMsg ==9:   msgSistema ='Proceso de copia realizado con Exito...'
    elif pcodMsg ==10:  msgSistema ='No existe periodo cerrado para realizar la Replica...'
    elif pcodMsg ==11:  msgSistema ='No existen registros, verifique...'
    elif pcodMsg ==12:  msgSistema ='Periodo a posponer debe ser mayor al actual...'
    elif pcodMsg ==13:  msgSistema ='ATENCION. Se debe suspender período para iniciar uno nuevo...'
    elif pcodMsg ==99:  msgSistema ='ATENCIÓN. Se produjo un Error. Informe al encargado...'
    else:
        msgSistema  ='Mensaje No Definido...'

    ctxmsgsist = {'msgTitulo': msgTitulo, 'msgSistema': msgSistema, 'tipMsg': ptipMsg}
    return render(request, 'fmhMsgSistema.html', ctxmsgsist)

# Gestion Financiera
# ==================
def fmh_Gestion(request):
    # Crea Formulario Periodo vacio.
    miFormPeriodo = FormSldPeriodo()

    # Capturando Session Periodo de Proceso
    if "periodo" in request.session:
        periodoProceso = request.session.get('periodo')
        desCtx =fncDevuelvemes(periodoProceso)

        # Funcion para traer ultimo periodo, devuelve una Lista
        cadenaPeriodo =list(fncUltimoPer())
        ultAngo = cadenaPeriodo[0]
        ultMes = cadenaPeriodo[1]
        mesUlt = fncNomMes(ultMes)

        # Asignar Contexto
        contextoPPROC = {'periodo': desCtx, 'ultAngo':ultAngo, 'ultMes':mesUlt, 'form': miFormPeriodo}

    else:
        descCtx ='...Periodo Cerrado...'
        contextoPPROC = {'periodo': descCtx, 'form': miFormPeriodo}

    return render(request, "fmhGestion.html", contextoPPROC)

# Ingresos Haberes
def fmhIngresosHab(request):
    # Recupera Periodo
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]
        pmes = cadenaFecha[-2:]
        pnmes = fncNomMes(pmes)

        if request.method == "POST":
            formIngreso = FormIngreso(request.POST)

            if formIngreso.is_valid():
                vingcodtipo = request.POST["ingcodtipo"]
                vingGlosa = request.POST["ingGlosa"]
                vingValor = request.POST["ingValor"]

                # contexto
                Ingresos = Fmhingreso.objects.create(ingango=pango, ingmes=pmes, ingcodtipo=vingcodtipo, \
                    ingGlosa=vingGlosa, ingValor=vingValor)

                return redirect('IngresoHab')

        else:
            formIngreso = FormIngreso()

        # Ingresos Realizados
        listIng = Fmhingreso.objects.filter(ingango__icontains=pango, ingmes__icontains=pmes).order_by('-id')

        # Suma de Ingresos
        ResultSum = Fmhingreso.objects.filter(ingango__icontains=pango, ingmes__icontains=pmes) \
            .aggregate(totalIng=Sum('ingValor'))

        TotSuma = ResultSum.get('totalIng', 0)

        contexto = {'Periodo': pango, 'Mes': pnmes, 'listing': listIng, 'SumIng': TotSuma, 'form': formIngreso}
        return render(request, 'fmhIngresosNew.html', contexto)
    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Formulario Ingreso Movimientos de Gastos
def fmhIngresoMvtos(request):
    # Recupera Periodo
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        vingango = cadenaFecha[0:4]
        vingmes = cadenaFecha[-2:]
        pnmes = fncNomMes(vingmes)

        if request.method == "POST":
            formIngMov = FormIngmvtos(request.POST)

            if formIngMov.is_valid():
                # Recupera request
                vcodtipo = request.POST["movcodtipo"]
                vglosa = request.POST["movglosa"]
                vmtomov = request.POST["movmto"]

                # contexto
                Movimientos = Fmhmovimiento.objects.create(movango=vingango, movmes=vingmes, movcodtipo=vcodtipo, \
                    movglosa=vglosa, movmto=vmtomov)

                # Genera Registro de Pago
                pagidref = Movimientos.id
                pagango = vingango
                pagmes = vingmes
                pagglosamov = Movimientos.movglosa
                pagmtomov = Movimientos.movmto
                pagestado = 0

                # Abre conexion BD y genera registro de Pagos
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("insert into hdagestion.gestionpedidos_fmhpago (pagango, pagmes, pagidrefmov, pagglosamov, pagmtomov, pagestado)" \
                        "values (%s, %s, %s, %s, %s, %s)", [pagango, pagmes, pagidref, pagglosamov, pagmtomov, pagestado])

                return redirect('IngresoDeb')

        else:
            # Crear Formulario vacio
            formIngMov = FormIngmvtos()

        # Movimientos Ingresados
        listMov = Fmhmovimiento.objects.filter(movango__icontains=vingango, movmes__icontains=vingmes).order_by('-id')

        # Total de Pagos Pendientes
        ResultPagos = Fmhmovimiento.objects.filter(movango__icontains=vingango, movmes__icontains=vingmes) \
            .aggregate(totalPdtes=Sum('movmto', filter=Q(movestado=False)))

        totPendiente = ResultPagos.get('totalPdtes', 0)
        if not totPendiente:
            totPendiente =0

        ctxMov = {'Periodo': vingango, 'Mes': pnmes, 'listmov': listMov, 'SumPag': totPendiente, 'form': formIngMov}
        return render(request, 'fmhIngresoMvtos.html', ctxMov)

    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Lista los Movimientos Ingresados en el Periodo
def fmhListaMov(request):

    # Recuperar periodo
    cadenaFecha = request.session.get('periodo')
    vango = cadenaFecha[0:4]
    vmes = cadenaFecha[-2:]

    listaMvtos = Fmhmovimiento.objects.filter(movango__icontains=vango, movmes__icontains=vmes).order_by('-id')
    return render(request, 'fmhListaMov.html', {"listing": listaMvtos, "query": vango, "query": vmes})

# Gestiona los registros del periodo ingresado
# elimina o actualiza
def fmhGestionIngreso(request):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]
        pmes = cadenaFecha[-2:]

        gestionIngresos = Fmhingreso.objects.filter(ingango__icontains=pango, ingmes__icontains=pmes).order_by('-id')

        if gestionIngresos:
            return render(request, 'fmhGestionIngresos.html', {'listing': gestionIngresos, 'query': pango, 'query': pmes})
        else:
            codmsg =11
            codtip ='W'
            return redirect('msgSistema',codmsg, codtip)

    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Vista que llama template para validar Eliminación del registro
def fmhEliminaId(request, pId, pAngo, pMes):
    
    ango =pAngo
    mes =pMes
    opc ='ING'

    contexto = {'verifId':pId, 'periodoAngo':ango, 'periodoMes':mes, 'opcion':opc}
    return render(request, 'fmhVerificaeliming.html', contexto)

# Elimina Registro de la Base de Datos
def eliminarBDIng(request, pId):
    registroElim=Fmhingreso.objects.get(id=pId)
    registroElim.delete()

    return redirect('gestionIngreso')

# Vuelve a listado ingresos
def vuelveGestionIng(request):
    return redirect('gestionIngreso')

# Formulario que Actualiza Ingresos
def fmhActualizaIng(request, pId):
    # recupera periodo
    cadenaFecha = request.session.get('periodo')

    pango = cadenaFecha[0:4]
    pmes = cadenaFecha[-2:]
    pnmes = fncNomMes(pmes)

    # guarda id de ingreso
    varIDngreso = pId

    # lee desde BD registro id y se instancia en un querySet
    try:
        QSingresos = Fmhingreso.objects.get(id=varIDngreso)
    except:
        varTitulo = 'Actualización de Ingresos'
        varSubtitulo = 'ATENCIÓN. Registro No Existe.'
        ctxPeriodo = {'msgTitulo': varTitulo, 'msgSubtitulo': varSubtitulo}
        return render(request, 'fmhMsgwarning.html', ctxPeriodo)            

    if request.method == "POST":
        # Actualizar formulario
        formIng = Formacting(request.POST, instance=QSingresos)

        if formIng.is_valid():
            formIng.save()
            return redirect('gestionIngreso')
        else:
            codmsg =99
            codtip ='S'
            return redirect('msgSistema',codmsg, codtip)
    else:
        # crear formulario con los datos recuperados
        formIng = Formacting(instance=QSingresos)

    ctxActIng = {'Periodo': pango, 'Mes': pnmes, 'form': formIng}
    return render(request, 'fmhActualizaing.html', ctxActIng)

# Eliminacion de Ingresos mediante checkbox
def ElimselallIng(request):
    if request.method == "POST":
        cont=0
        data=request.POST.getlist('estcheck')

        if data:            
            for numId in data:
                cont +=1

                try:
                    regElimIngresos = Fmhingreso.objects.get(id=numId)
                    regElimIngresos.delete()
                except regElimIngresos.DoesNotExist:
                    docu ="No existe Registro. Verifique"
                    return HttpResponse(docu)

            return redirect('gestionIngreso')

        else:
            codmsg =4
            codtip ='S'
            return redirect('msgSistema',codmsg, codtip)

    else:
        docu="NO POST"
    
    return HttpResponse(docu)

# ===========
# Movimientos
# ===========

# ===============================
# Funcion, Vista basada en Clases
# ===============================
"""
class fmhGestionMvtosList(ListView):
    model = Fmhmovimiento
    template_name = 'fmhGestionMvtos.html'

    def get_queryset(self):

        if "periodo" in self.request.session:
            cadenaFecha = self.request.session.get('periodo')

            # Recupera Periodo
            pango = cadenaFecha[0:4]
            pmes = cadenaFecha[-2:]

            return self.model.objects.filter(movango__icontains=pango, movmes__icontains=pmes).order_by('-id')

        else:
            pass
"""
# Listado de movimientos ingresados (Funcion)
def fmhGestionMvtos(request, pEstado):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]
        pmes = cadenaFecha[-2:]

        # Filtro por estado de Pago.
        if pEstado ==3:
            gestionMov = Fmhmovimiento.objects.filter(movango__icontains=pango, movmes__icontains=pmes).order_by('-id')
        else:
            gestionMov = Fmhmovimiento.objects.filter(movango__icontains=pango, movmes__icontains=pmes, movestado__icontains=pEstado).order_by('-id')

        if not gestionMov:
            codmsg =11
            codtip ='W'
            return redirect('msgSistema',codmsg, codtip)
        else:
            # Sumatoria de Pagos agrupado por estado de movimiento.
            resultPagos = Fmhmovimiento.objects.filter(movango__icontains=pango, movmes__icontains=pmes) \
                .aggregate(
                            totalPagado=Sum('movmto', filter=Q(movestado=True)),
                            totalPdte=Sum('movmto', filter=Q(movestado=False))
                            )

            totPagado = resultPagos.get('totalPagado', 0)
            totPdte = resultPagos.get('totalPdte', 0)

            if not totPagado:
                totPagado =0
            if not totPdte:
                totPdte =0

            contextoMvtos = {'listing': gestionMov, 'STotPag': totPagado, 'STotPdte': totPdte}
            return render(request, 'fmhGestionMvtos.html', contextoMvtos)

    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Vista que llama template para validar Eliminación del registro de movimientos
def fmhEliminaIdmov(request, pId, pAngo, pMes):
    
    ango =pAngo
    mes =pMes
    opc ='MOV'

    contexto = {'verifId': pId, 'periodoAngo': ango, 'periodoMes': mes, 'opcion':opc}
    return render(request, 'fmhVerificaeliming.html', contexto)

# Vista Elimina Registro de la Base de Datos (Movimientos)
def eliminarBDMov(request, pId):
    # Elimina registro movimientos
    registroElim=Fmhmovimiento.objects.get(id=pId)
    registroElim.delete()

    # Elimina registro de Pagos
    fncElimPagos(pId)

    estadoPago =3
    return redirect('gestionMovimientos', estadoPago)

# Eliminacion de Movimientos mediante checkbox
def ElimselallMov(request):
    if request.method == "POST":
        cont=0
        data=request.POST.getlist('estcheck')

        if data:            
            for numId in data:
                cont +=1

                try:
                    regElimMvtos = Fmhmovimiento.objects.get(id=numId)
                    regElimMvtos.delete()

                    # Elimina registro de Pagos
                    fncElimPagos(numId)

                except regElimMvtos.DoesNotExist:
                    docu ="No existe Registro. Verifique"
                    return HttpResponse(docu)

            estadoPago =3
            return redirect('gestionMovimientos', estadoPago)

        else:
            codmsg =4
            codtip ='S'
            return redirect('msgSistema',codmsg, codtip)
    else:
        docu="NO POST"
    
    return HttpResponse(docu)

# Formulario Edicion Movimientos
def fmhActualizaMov(request, pId):
    # recupera periodo
    cadenaFecha = request.session.get('periodo')

    pango = cadenaFecha[0:4]
    pmes = cadenaFecha[-2:]
    pnmes = fncNomMes(pmes)

    # guarda id de ingreso
    varIDmvto = pId
    estadoPago =3

    # lee desde BD registro id y se instancia en un querySet (Movimientos)
    try:
        QSmvtos = Fmhmovimiento.objects.get(id=varIDmvto)
    except:
        varTitulo = 'Actualización de Movimientos'
        varSubtitulo = 'ATENCIÓN. Registro No Existe.'
        ctxPeriodo = {'msgTitulo': varTitulo, 'msgSubtitulo': varSubtitulo}
        return render(request, 'fmhMsgwarning.html', ctxPeriodo)            

    if request.method == "POST":
        # Actualizar formulario
        formMov = Formmvtos(request.POST, instance=QSmvtos)

        if formMov.is_valid():
            formMov.save()

            # Actualizo Monto del Pago en caso de haber actualizado Movimientos
            tipoMov = QSmvtos.movcodtipo
            concepto = QSmvtos.movglosa
            mtoPago = QSmvtos.movmto
            fncActualizaPagos(varIDmvto, concepto, mtoPago)

            return redirect('gestionMovimientos', estadoPago)
    else:
        # crear formulario con los datos recuperados
        formMov = Formmvtos(instance=QSmvtos)

    ctxEdiMov = {'Periodo': pango, 'Mes': pnmes, 'form': formMov}
    return render(request, 'fmhEditaMvtos.html', ctxEdiMov)

# =====
# Pagos
# =====

# Listado de pagos pendientes
def fmhListPagPen(request):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]
        pmes = cadenaFecha[-2:]

        estadoPago =0 # Pagos pendientes
        listadoPagos = Fmhpago.objects.filter(pagango__icontains=pango, pagmes__icontains=pmes, pagestado__icontains=estadoPago).order_by('-id')

        # Suma variable pagmtomov y devuelve un diccionario
        SumaPagos = Fmhpago.objects.filter(pagango__icontains=pango, pagmes__icontains=pmes, pagestado__icontains=estadoPago).aggregate(Sum('pagmtomov'))
        totalSum = SumaPagos.values()

        if listadoPagos:
            # Formulario Periodo para posponer el pago
            fNewPag = FormSldPeriodo()

            contexto = {"listing": listadoPagos, "pagPdtes": totalSum, 'form': fNewPag}
            return render(request, 'fmhInfPagos.html', contexto)
        else:
            varTitulo = 'PAGO DE SERVICIOS'
            varSubtitulo = 'ATENCIÓN. No existen registros pendientes de pago'
            ctxPeriodo = {'msgTitulo': varTitulo, 'msgSubtitulo': varSubtitulo}

    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

    return render(request, 'fmhMsgwarning.html', ctxPeriodo)

# Pago de Documentos
def fmhPagoDcto(request, pId, pIdref):
    # guarda id de pago
    varIDpago = pId
    varIdRefer = pIdref

    try:
        QSpagos = Fmhpago.objects.get(id=varIDpago)
    except:
        varTitulo = 'Pago de Documentos'
        varSubtitulo = 'ATENCIÓN. Registro No Existe.'
        ctxPeriodo = {'msgTitulo': varTitulo, 'msgSubtitulo': varSubtitulo}
        return render(request, 'fmhMsgwarning.html', ctxPeriodo)            

    if request.method == "POST":
        # Actualizamos el Formulario
        formpagos = Formpagos(request.POST, instance=QSpagos)

        if formpagos.is_valid():
            formpagos.save()

            # Actualizar Movimientos con estado pagado para id pagado
            from django.db import connection
            with connection.cursor() as pag:

                pag.execute("update hdagestion.gestionpedidos_fmhmovimiento set movestado =%s" \
                    " where id = %s", [1, varIdRefer])

            # Redireccionamos a la lista de pagos pendientes.
            return redirect('listaPagPend')
        else:
            valorMtopago = QSpagos.pagmtopago
            numdocu = QSpagos.pagnumdocu

            if valorMtopago <0:
                varTitulo = 'Pago de Documentos'
                varSubtitulo = 'ATENCIÓN. Monto del pago no puede ser Negativo'
                ctxPeriodo = {'msgTitulo': varTitulo, 'msgSubtitulo': varSubtitulo}
            elif len(str(numdocu)) >10:

                varTitulo = 'Pago de Documentos'
                varSubtitulo = 'ATENCIÓN. Excede el máximo de caracteres en el Numero de Dcto. '
                ctxPeriodo = {'msgTitulo': varTitulo, 'msgSubtitulo': varSubtitulo}

            return render(request, 'fmhMsgwarning.html', ctxPeriodo)            

    else:
        QSpagos.pagmtopago =''
        QSpagos.pagfecha = datetime.now()

        # crear formulario con los datos recuperados
        formPagos = Formpagos(instance=QSpagos)

    # direcciona al template con formulario
    return render(request, 'fmhRealizaPago.html', {'form': formPagos})

# Vuelve a listado movimientos
def vuelveGestionMov(request):
    estadoPago =3
    return redirect('gestionMovimientos', estadoPago)

# Posponer el pago a futuro
def fmhPosponerPago(request):
    cadenaFecha = fncSession(request)

    pango = cadenaFecha[0:4]
    pmes = cadenaFecha[-2:]

    if request.method =="POST":
        vAngoNew = request.POST['periodo']
        vMesNew = request.POST['meses']
        vIdPago = request.POST['id_idMod']
        vIdRefP = request.POST['id_idRef']

        if int(pango) <= int(vAngoNew) and int(pmes) < int(vMesNew):
            # Posponer pago
            from django.db import connection
            with connection.cursor() as posp:
            
                # Posponer Movimientos
                try:
                    posp.execute("update hdagestion.gestionpedidos_fmhmovimiento set movango =%s, movmes =%s" \
                        " where id = %s", [vAngoNew, vMesNew, vIdRefP])
                except:
                    codmsg =99
                    codtip ='S'
                    return redirect('msgSistema',codmsg, codtip)

                # Posponer Pago
                try:
                    posp.execute("update hdagestion.gestionpedidos_fmhpago set pagango =%s, pagmes =%s" \
                        " where id = %s", [vAngoNew, vMesNew, vIdPago])
                except:
                    codmsg =99
                    codtip ='S'
                    return redirect('msgSistema',codmsg, codtip)

                return redirect('listaPagPend')

        else:
            codmsg =12
            codtip ='S'
            return redirect('msgSistema',codmsg, codtip)

def fmhSaldosPeriodo(request):
    if request.method=="GET":
        varPeriodo = request.GET['periodo']
        varMeses = request.GET['meses']
        return redirect('consultasaldos', varPeriodo, varMeses)

# Consulta Saldos del Periodo
def fmhSaldos(request, parango, parmes):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        formularioSaldos = FormSldPeriodo()

        if parango ==0:
            # Viene dese el Menu Principal
            pango = cadenaFecha[0:4]
            pmes = cadenaFecha[-2:]
        else:
            # Viene desde formulario consulta Saldos
            pango = parango
            pmes = fncMes(parmes)
            cadenaFecha =str(pango)+str(pmes)

        nommes = fncNomMes(pmes)
        periodoSld = fncDevuelvemes(cadenaFecha)

        sldEnc = Fmhsldenc.objects.filter(sldango__icontains=pango, sldmes__icontains=pmes)
        sldDet = Fmhslddet.objects.filter(sdeango__icontains=pango, sdemes__icontains=pmes)

        contextoSld = {'listing':sldEnc, 'listDet':sldDet, 'NombreMes':nommes, 'PeriodoSld':periodoSld, 'form': formularioSaldos}

        return render(request, 'fmhSaldos.html', contextoSld)
    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Formulario que renderiza replica
def fmhreplica(request):
    # Recupera Periodo del Formulario
    if request.method =="GET":
        forango = request.GET["periodo"]
        formes = request.GET["meses"]

        return redirect('replicaPeriodo', forango, formes)

# Copia ultimo movimiento a un nuevo periodo
def fmhCopiaMovPag(request, newpango, newpmes):
    # Captura  Session
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]
        pmes = cadenaFecha[-2:]
        newpmes =fncMes(newpmes)

        # Funcion para traer ultimo periodo, devuelve una Lista
        cadenaPeriodo =list(fncUltimoPer())
        ultAngo = cadenaPeriodo[0]
        ultMes = cadenaPeriodo[1]

        if ultAngo !='X':
            pestado =0

            # Valida que periodo ingresado no exista en tabla Movimientos.
            resultMvtos = Fmhmovimiento.objects.filter(movango__icontains=newpango, movmes__icontains=newpmes)
            existeMov = resultMvtos.values()

            if not existeMov:
                try:
                    fncCopiaPeriodo(newpango, newpmes, ultAngo, ultMes, pestado)
                    codmsg =9
                    codtip ='O'
                    return redirect('msgSistema',codmsg, codtip)

                except:
                    codmsg =99
                    codtip ='S'
                    return redirect('msgSistema',codmsg, codtip)

            else:
                codmsg =5
                codtip ='S'
                return redirect('msgSistema',codmsg, codtip)
        else:
            codmsg =10
            codtip ='S'
            return redirect('msgSistema',codmsg, codtip)

    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

    return redirect('gestionHogar')

# Cierre de Proceso Mensual
def fmhcierreProc(request):
    # Capturando Session
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]
        pmes = cadenaFecha[-2:]

        # Validar si periodo actual no se encuentra ejecutado.
        if not fncValPerProc(pango, pmes):
            # Importamos conexion
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.callproc('prcCierremensual', (pango, pmes))

                # Borro Elemento de Session
                del request.session['periodo']
                # Purga la eliminacion de la base de datos.
                request.session.flush()

                codmsg =8
                codtip ='O'
                return redirect('msgSistema',codmsg, codtip)
        else:
            codmsg =3
            codtip ='S'
            return redirect('msgSistema',codmsg, codtip)
    else:
        codmsg =2
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# ============
# Estadisticas
# ============

# Ingresos, Egresos y Saldos
def fmhObtieneSaldos(request):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]

        slding = list()
        sldegr = list()
        saldos = list()

        for mes in range(1, 13):
            mesaux = fncMes(mes)
            nommes = fncNomMes(mesaux)

            dataset = Fmhsldenc.objects.filter(sldango__icontains=pango, sldmes__icontains=mesaux).order_by('sldmes')
            if dataset:
                for entry in dataset:
                    slding.append(entry.sldingresos)
                    sldegr.append(entry.sldegresos)
                    saldos.append(entry.sldsaldo)
            else:
                #sldmes.append(nommes)
                slding.append(0)
                sldegr.append(0)
                saldos.append(0)
        
        return render(request, 'fmhEstadisticaSld.html', {
            'periodo': json.dumps(int(pango)),
            'slding': json.dumps(slding),
            'sldegr': json.dumps(sldegr),
            'saldos': json.dumps(saldos)
            })
    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Estadistica por tipo de Gasto
def fmhEstadGastos(request):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        pango = cadenaFecha[0:4]

        gtoMensual = list()

        # Data Gastos Mensuales
        for mes in range(1, 13):
            mesaux = fncMes(mes)
            nommes = fncNomMes(mesaux)

            dataset = Fmhestadgasto.objects.filter(estadango__icontains=pango, estadmes__icontains=mesaux).order_by('estadmes')
            if dataset:
                for entry in dataset:
                    totMensual = (entry.estadgto1+entry.estadgto2+entry.estadgto3+entry.estadgto4+entry.estadgto5+
                                entry.estadgto6+entry.estadgto7+entry.estadgto8+entry.estadgto9)

                    gtoMensual.append(totMensual)
            else:
                gtoMensual.append(0)

        # Data Gastos Anuales por Concepto
        lgto1 = list()

        dataAnual = Fmhestadgasto.objects.filter(estadango__icontains=pango) \
            .aggregate(
                totFin=Sum('estadgto1'),
                totFij=Sum('estadgto2'),
                totAut=Sum('estadgto3'),
                totTec=Sum('estadgto4'),
                totGme=Sum('estadgto5'),
                totCol=Sum('estadgto6'),
                totSup=Sum('estadgto7'),
                totCon=Sum('estadgto8'),
                totOga=Sum('estadgto9')
            )

        totalFin = dataAnual.get('totFin', 0)
        totalFij = dataAnual.get('totFij', 0)
        totalAut = dataAnual.get('totAut', 0)
        totalTec = dataAnual.get('totTec', 0)
        totalGme = dataAnual.get('totGme', 0)
        totalCol = dataAnual.get('totCol', 0)
        totalSup = dataAnual.get('totSup', 0)
        totalCon = dataAnual.get('totCon', 0)
        totalOga = dataAnual.get('totOga', 0)

        lgto1.append(totalFin)
        lgto1.append(totalFij)
        lgto1.append(totalAut)
        lgto1.append(totalTec)
        lgto1.append(totalGme)
        lgto1.append(totalCol)
        lgto1.append(totalSup)
        lgto1.append(totalCon)
        lgto1.append(totalOga)

        # Data Grilla Gastos Mensuales
        datasetGM = Fmhestadgasto.objects.filter(estadango__icontains=pango).order_by('estadmes')

        # Totalizador por Mes
        gEne = gtoMensual[0]
        gFeb = gtoMensual[1]
        gMar = gtoMensual[2]
        gAbr = gtoMensual[3]
        gMay = gtoMensual[4]
        gJun = gtoMensual[5]
        gJul = gtoMensual[6]
        gAgo = gtoMensual[7]
        gSep = gtoMensual[8]
        gOct = gtoMensual[9]
        gNov = gtoMensual[10]
        gDic = gtoMensual[11]

        # Data Gastos Anuales por Concepto (Grafico de Pie)
        ceptoGMPORC = []
        dataGMPORC = []

        # Genera Conceptos
        ceptoGMPORC.append('Financieros')
        ceptoGMPORC.append('Fijos')
        ceptoGMPORC.append('Autopistas')
        ceptoGMPORC.append('Tecnología')
        ceptoGMPORC.append('Gastos Médicos')
        ceptoGMPORC.append('Colegios')
        ceptoGMPORC.append('Supermercado')
        ceptoGMPORC.append('Contribuciones')
        ceptoGMPORC.append('Otros Gastos')

        datasetGMPORC = Fmhevolgasto.objects.filter(evolagno__icontains=pango)
        if datasetGMPORC:
            for cepto in datasetGMPORC:
                dataGMPORC.append(cepto.evolcepto1)
                dataGMPORC.append(cepto.evolcepto2)
                dataGMPORC.append(cepto.evolcepto3)
                dataGMPORC.append(cepto.evolcepto4)
                dataGMPORC.append(cepto.evolcepto5)
                dataGMPORC.append(cepto.evolcepto6)
                dataGMPORC.append(cepto.evolcepto7)
                dataGMPORC.append(cepto.evolcepto8)
                dataGMPORC.append(cepto.evolcepto9)
        else:
            dataGMPORC.append(0)        

        # Renderizado
        return render(request, 'fmhEstadGastos.html', {
                'periodo': json.dumps(int(pango)),
                'GastosMensuales': json.dumps(gtoMensual),
                'Gastos': json.dumps(lgto1),
                'listGM': datasetGM,
                # Totales Mensuales
                'lgEne': gEne,
                'lgFeb': gFeb,
                'lgMar': gMar,
                'lgAbr': gAbr,
                'lgMay': gMay,
                'lgJun': gJun,
                'lgJul': gJul,
                'lgAgo': gAgo,
                'lgSep': gSep,
                'lgOct': gOct,
                'lgNov': gNov,
                'lgDic': gDic,
                # Totales anuales
                'taFin': totalFin,
                'taFij': totalFij,
                'taAut': totalAut,
                'taTec': totalTec,
                'taGme': totalGme,
                'taCol': totalCol,
                'taSup': totalSup,
                'taCon': totalCon,
                'taOga': totalOga,
                # Totales Anuales por concepto (grafico de pie)
                'conceptos': ceptoGMPORC, 
                'data': dataGMPORC
                })

    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Creacion de session periodo de proceso
def fmhCreasession(request):

    if request.user.is_authenticated:

        if request.method == "POST":
            periodoCompuesto = request.POST["periodoango"] + request.POST["periodomes"]

            pango = periodoCompuesto[0:4]
            pmes = periodoCompuesto[-2:]

            # Validar si periodo actual no se encuentra ejecutado.
            if not fncValPerProc(pango, pmes):
                # Validando si existe session 
                if "periodo" in request.session:
                    # Periodo abierto, se debe cerrar sesion
                    codmsg =13
                    codtip ='W'
                    return redirect('msgSistema',codmsg, codtip)
                else:
                    # Creando sesion
                    request.session['periodo'] = periodoCompuesto
            else:
                codmsg =3
                codtip ='S'
                return redirect('msgSistema',codmsg, codtip)

            # Redireccionando al origen
            return redirect('gestionHogar')

    else:
        return redirect('login')

# Cierra Session Periodo de proceso
def fmhsuspendeSess(request):

    # Validando si existe session 
    if "periodo" in request.session:
        # Borro Elemento de Session
        del request.session['periodo']
        # Purga la eliminacion de la base de datos.
        request.session.flush()

        # Se desloguea al usuario
        return redirect('logout')

    else:
        codmsg =2
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)

# Consulta General, obtiene request del formulario
def fmhConsGral(request):
    if request.method=="GET":
        varPeriodo = request.GET['periodo']
        varMeses = request.GET['meses']
        return redirect('consulta_gral', varPeriodo, varMeses)

# Consulta General (Ingresos, Movimientos, Pagos y Grafico de Saldos)
def fmhConsultaGral(request,  parango, parmes):
    cadenaFecha = fncSession(request)

    if cadenaFecha !='000000':
        formConsGral = FormSldPeriodo()

        if parango ==0:
            # Viene dese el Menu Principal
            pango = cadenaFecha[0:4]
            pmes = cadenaFecha[-2:]
        else:
            # Viene desde formulario consulta Saldos
            pango = parango
            pmes = parmes
            cadenaFecha =str(pango)+str(pmes)

        periodoCons = fncDevuelvemes(cadenaFecha)

        # Ingresos
        resultIng = Fmhingreso.objects.filter(ingango__icontains=pango, ingmes__icontains=pmes).order_by('id')
       
        # Pagos
        resultPag = Fmhpago.objects.filter(pagango__icontains=pango, pagmes__icontains=pmes).order_by('-pagfecha')

        # Etadistica Saldos Anuales
        saldos = list()

        for utm in range(1, 13):
            pmes = fncMes(utm)

            dataset = Fmhsldenc.objects.filter(sldango__icontains=pango, sldmes__icontains=pmes)
            if dataset:
                for entry in dataset:
                    saldos.append(entry.sldsaldo)
            else:
                saldos.append(0)

        contextoCGral = {'listing': resultIng, 'listpag': resultPag, 'periodo': periodoCons,
                'periodoGR': json.dumps(int(pango)),
                'saldos': json.dumps(saldos),
                'form': formConsGral}
            
        return render(request, 'fmhConsGral.html', contextoCGral)
    else:
        codmsg =1
        codtip ='W'
        return redirect('msgSistema',codmsg, codtip)