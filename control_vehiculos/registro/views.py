from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.timezone import now, make_aware,localtime
from django.utils.dateparse import parse_datetime
from .models import RegistroVehiculo, RegistroCamiones, RegistroAdministrativos
from .google_drive_utils import update_excel
from datetime import datetime
import pandas as pd
from django.db.models import Q
from django.contrib import messages

# Página principal
def pagina_principal(request):
    return render(request, 'registro/pagina_principal.html')

from .models import RegistroVehiculo

def leer_datos_excel(sheet_name=None):
    """
    Obtiene los datos de la base de datos y los devuelve en formato de lista de diccionarios.
    """
    if sheet_name == "Vehiculos":
        # Leer datos de la base de datos
        data = RegistroVehiculo.objects.all().values(
            "id", "entrada", "dni", "apellido_nombre", "empresa",
            "pte_numero", "ingreso_remitos", "egreso_remitos", "salida_vehiculo"
        )
        return list(data) 
    else:
        # Implementa otros casos si tienes múltiples tablas
        raise ValueError(f"No se reconoce el nombre de la hoja: {sheet_name}")
    
def  leer_datos_excel_camiones(sheet_name=None):
    if sheet_name=="Camiones":
        data=RegistroCamiones.objects.all().values(
            "id","chofer","tractor","semi","dni","egreso","egreso2","egreso3",
            "ingreso","ingreso2","ingreso3","transporte"
        )
        return list(data)
    else:
        raise ValueError(f"No se reconoce el nombre de la hoja: {sheet_name}")

def listar_datos_camiones(request):
    try:
        datos_camiones = leer_datos_excel_camiones(sheet_name="Camiones")
        return render(request, 'registro/Control de Camiones.html', {'camiones': datos_camiones})
    except Exception as e:
        print(f"Error al listar camiones: {e}")
        return HttpResponse("Error al listar camiones.", status=500)


def control_vehiculos(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            entrada = request.POST.get('entrada')
            dni = request.POST.get('dni')
            pte_numero = request.POST.get('pte_numero')
            apellido_nombre = request.POST.get('apellido_nombre')
            empresa = request.POST.get('empresa')
            ingreso_remitos = request.POST.get('ingreso_remitos')

            # Validar campos obligatorios
            if not entrada or not dni:
                messages.error(request, "Error: Faltan campos requeridos.")
                return redirect(reverse('control_vehiculos')) 
            # Crear el registro en la base de datos
            vehiculo = RegistroVehiculo.objects.create(
                entrada=parse_datetime(entrada),
                dni=dni,
                pte_numero=pte_numero,
                apellido_nombre=apellido_nombre,
                empresa=empresa,
                ingreso_remitos=ingreso_remitos
            )

            # Datos organizados para enviar al Excel
            data = [
                vehiculo.id,                # ID
                vehiculo.dni,               # DNI
                vehiculo.entrada.strftime('%Y-%m-%d %H:%M') if vehiculo.entrada else '',  # Entrada
                vehiculo.apellido_nombre,   # Apellido y Nombre
                vehiculo.empresa,           # Empresa
                vehiculo.ingreso_remitos,   # Ingreso Remitos
                vehiculo.pte_numero,        # Nro de Patente
                vehiculo.egreso_remitos or '',  # Egreso Remitos (inicialmente vacío)
                vehiculo.salida_vehiculo.strftime('%Y-%m-%d %H:%M') if vehiculo.salida_vehiculo else '',
            ]

            # Llamar a la función de actualización del Excel
            update_excel(data, "Vehiculos")

            print("Datos enviados al Excel:", data)  # Depuración
            messages.success(request, "Datos registrados con éxito.")
            return redirect(reverse('listar_vehiculos_pendientes'))
        except Exception as e:
            import traceback
            print(f"Error al registrar: {e}")
            traceback.print_exc()
            messages.error(request, "Error interno del servidor.")
            return redirect(reverse('control_vehiculos'))
    return render(request, 'registro/Control de Ingreso y Egreso de Vehículos.html')


# Control de camiones
from django.urls import reverse
from django.contrib import messages
from datetime import datetime

def control_camiones(request):
    if request.method == 'POST':
        try:
            print("Iniciando registro de camión...")

            # Captura los datos del formulario
            ingreso = datetime.now() 
            chofer = request.POST.get('chofer', None)
            dni = request.POST.get('dni_chofer', None)
            transporte = request.POST.get('transporte', None)
            tractor = request.POST.get('tractor', None)
            semi = request.POST.get('semi', None)

            # Validación de campos obligatorios
            if not dni:
                messages.error(request, "Error: El DNI del chofer es obligatorio.")
                return redirect(reverse('control_camiones'))

            # Crear y guardar el registro del camión
            camion = RegistroCamiones(
                ingreso=ingreso,
                chofer=chofer,
                dni=dni,
                transporte=transporte,
                tractor=tractor,
                semi=semi
            )
            camion.save()

            print(f"Camión registrado con ID: {camion.id}")

            data = [
                camion.id,
                camion.chofer,
                camion.dni,
                camion.tractor,
                camion.semi,
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.transporte,
                camion.egreso.strftime('%Y-%m-%d %H:%M') if camion.egreso else '',
                camion.ingreso2 or '',
                camion.egreso2 or '',
                camion.ingreso3 or '',
                camion.egreso3 or '',
            ]
            print(f"Datos para actualizar Excel: {data}")

            update_excel(data, "Camiones")
            print("Datos actualizados en el Excel.")

            messages.success(request, "Datos registrados con éxito.")
            return redirect(reverse('listar_camiones_pendientes'))

        except RegistroCamiones.DoesNotExist:
            print("Error: RegistroCamiones no existe.")
            messages.error(request, "Error: Registro no encontrado.")
            return HttpResponse("Error: Camión no encontrado.", status=404)

        except Exception as e:
            import traceback
            print("Error al registrar el camión:")
            traceback.print_exc()  # Muestra el error completo en la consola
            messages.error(request, f"Error interno del servidor: {str(e)}")
            return redirect(reverse('control_camiones'))

    return render(request, 'registro/Control de Camiones.html')


# Control de administrativos
def control_administrativos(request):
    if request.method == 'POST':
        try:
            print("Iniciando registro de administrativo...")

            # Captura los datos del formulario
            entrada_admin1 = datetime.now()  # Fecha actual naive
            vehiculo = request.POST.get('vehiculo', None)
            patente = request.POST.get('patente', None)
            apellido_nombre_admin = request.POST.get('apellido_nombre_admin', None)
            observaciones = request.POST.get('observaciones', None)

            # Validación de campos obligatorios
            if not apellido_nombre_admin:
                messages.error(request, "Error: El nombre del administrativo es obligatorio.")
                return redirect(reverse('control_administrativos'))

            # Crear y guardar el registro del administrativo
            administrativo = RegistroAdministrativos(
                entrada_admin1=entrada_admin1,
                vehiculo=vehiculo,
                patente=patente,
                apellido_nombre_admin=apellido_nombre_admin,
                observaciones=observaciones
            )
            administrativo.save()

            print(f"Administrativo registrado con ID: {administrativo.id}")

            datos = [
                administrativo.id,
                administrativo.entrada_admin1.strftime('%Y-%m-%d %H:%M') if administrativo.entrada_admin1 else '',
                administrativo.vehiculo or '',
                administrativo.patente or '',
                administrativo.apellido_nombre_admin or '',
                administrativo.observaciones or '',
                administrativo.salida_admin1.strftime('%Y-%m-%d %H:%M') if administrativo.salida_admin1 else '',
                administrativo.entrada_admin2.strftime('%Y-%m-%d %H:%M') if administrativo.entrada_admin2 else '',
                administrativo.salida_admin2.strftime('%Y-%m-%d %H:%M') if administrativo.salida_admin2 else '',
            ]
            print(f"Datos para actualizar Excel: {datos}")

            update_excel(datos, "Administrativos")
            print("Datos actualizados en el Excel.")

            messages.success(request, "Administrativo registrado con éxito.")
            return redirect(reverse('listar_vehiculos_admin_pendientes'))

        except RegistroAdministrativos.DoesNotExist:
            print("Error: RegistroAdministrativos no existe.")
            messages.error(request, "Error: Registro no encontrado.")
            return HttpResponse("Error: Administrativo no encontrado.", status=404)

        except Exception as e:
            import traceback
            print("Error al registrar el administrativo:")
            traceback.print_exc()  # Muestra el error completo en la consola
            messages.error(request, f"Error interno del servidor: {str(e)}")
            return redirect(reverse('control_administrativos'))

    return render(request, 'registro/Administrativos de Softys.html')

def listar_administrativos(request):
    return render(request, 'registro/Administrativos de Softys.html')


def leer_datos_excel_admin(sheet_name=None):

    if sheet_name == "Administrativos":
        # Leer datos de la base de datos
        data = RegistroAdministrativos.objects.all().values(
            "vehiculo", "patente", "apellido_nombre_admin", "observaciones", "entrada_admin2",
            "salida_admin1", "salida_admin2", "entrada_admin1","id"
        )
        return list(data) 
    else:
        # Implementa otros casos si tienes múltiples tablas
        raise ValueError(f"No se reconoce el nombre de la hoja: {sheet_name}")

def leer_datos_excel_camiones(sheet_name=None):

    if sheet_name == "Camiones":
        # Leer datos de la base de datos
        data = RegistroCamiones.objects.all().values(
            "id", "chofer", "transporte", "semi", "dni",
            "egreso", "egreso2", "egreso3","ingreso","ingreso2","ingreso3"
        )
        return list(data) 
    else:
        # Implementa otros casos si tienes múltiples tablas
        raise ValueError(f"No se reconoce el nombre de la hoja: {sheet_name}")

from django.utils.timezone import localtime, now

def registrar_remitos(request, id):
    if request.method == 'POST':
        egreso_remitos = request.POST.get('egreso_remitos', None)

        try:
            # Buscar el vehículo por su ID
            vehiculo = RegistroVehiculo.objects.get(id=id)

            # Actualizar el campo de remitos
            vehiculo.egreso_remitos = egreso_remitos  # Usar la fecha/hora con zona horaria local
            vehiculo.save()

            # Datos para el Excel
            datos_vehiculo = [
                vehiculo.id,
                vehiculo.dni or '',
                vehiculo.entrada.strftime('%Y-%m-%d %H:%M') if vehiculo.entrada else '',
                vehiculo.apellido_nombre or '',
                vehiculo.empresa or '',
                vehiculo.ingreso_remitos or '',
                vehiculo.pte_numero or '',
                vehiculo.egreso_remitos or '',
                vehiculo.salida_vehiculo.strftime('%Y-%m-%d %H:%M') if vehiculo.salida_vehiculo else '',
            ]

            update_excel(datos_vehiculo, "Vehiculos")

            print(f"Remitos registrados y Excel actualizado con la hora local: {egreso_remitos}")
            return redirect('listar_vehiculos_pendientes')

        except RegistroVehiculo.DoesNotExist:
            print(f"No se encontró un vehículo con el ID: {id}")
            return HttpResponse("Error: Vehículo no encontrado.", status=404)


from django.utils.timezone import localtime, now

def registrar_salida(request, id):
    if request.method == 'POST':
        try:
            vehiculo = RegistroVehiculo.objects.get(id=id)

            # Registrar la salida con la fecha y hora actual convertida a naive (sin tzinfo)
            salida_vehiculo = datetime.now()

            vehiculo.salida_vehiculo = salida_vehiculo
            vehiculo.save()

            # Actualizar Excel
            datos_vehiculo = [
                vehiculo.id,
                vehiculo.dni or '',
                vehiculo.entrada.strftime('%Y-%m-%d %H:%M') if vehiculo.entrada else '',
                vehiculo.apellido_nombre or '',
                vehiculo.empresa or '',
                vehiculo.ingreso_remitos or '',
                vehiculo.pte_numero or '',
                vehiculo.egreso_remitos or '',
                vehiculo.salida_vehiculo.strftime('%Y-%m-%d %H:%M') if vehiculo.salida_vehiculo else ''
            ]

            # Llamada para actualizar Excel
            update_excel(datos_vehiculo, "Vehiculos")

            return redirect('listar_vehiculos_pendientes')

        except RegistroVehiculo.DoesNotExist:
            return HttpResponse("Error: Vehículo no encontrado.", status=404)

    return HttpResponse("Error al procesar la salida.", status=500)



from django.utils.timezone import localtime, now

def registrar_salida_admin(request, id):
    if request.method == 'POST':
        try:
            administrativo = RegistroAdministrativos.objects.get(id=id)
            # Registrar la salida con la fecha y hora actual convertida a naive (sin tzinfo)
            salida_admin1 = datetime.now()

            administrativo.salida_admin1 = salida_admin1  # Guardar fecha naive
            administrativo.save()

            datos_administrativo = [
                administrativo.id,
                administrativo.entrada_admin1.strftime('%Y-%m-%d %H:%M') if administrativo.entrada_admin1 else '',
                administrativo.vehiculo or '',
                administrativo.patente or '',
                administrativo.apellido_nombre_admin or '',
                administrativo.observaciones or '',
                administrativo.salida_admin1.strftime('%Y-%m-%d %H:%M') if administrativo.salida_admin1 else '',
                administrativo.entrada_admin2.strftime('%Y-%m-%d %H:%M') if administrativo.entrada_admin2 else '',
                administrativo.salida_admin2.strftime('%Y-%m-%d %H:%M') if administrativo.salida_admin2 else '',
            ]

            update_excel(datos_administrativo, "Administrativos")
            return redirect('listar_vehiculos_admin_pendientes')
        except RegistroAdministrativos.DoesNotExist:
            return HttpResponse("Error: Administrativo no encontrado.", status=404)
    return HttpResponse("Error al procesar la salida.", status=500)

# Función para registrar entrada 2 del administrativo
def registrar_entrada_admin2(request, id):
    if request.method == 'POST':
        try:
            administrativos = RegistroAdministrativos.objects.get(id=id)
            # Registrar la entrada con la fecha y hora actual convertida a naive (sin tzinfo)
            entrada_admin2 = datetime.now()

            administrativos.entrada_admin2 = entrada_admin2  # Guardar fecha naive
            administrativos.save()

            datos_vehiculo_admin = [
                administrativos.id,
                administrativos.entrada_admin1.strftime('%Y-%m-%d %H:%M') if administrativos.entrada_admin1 else '',
                administrativos.vehiculo or '',
                administrativos.patente or '',
                administrativos.apellido_nombre_admin or '',
                administrativos.observaciones or '',
                administrativos.salida_admin1.strftime('%Y-%m-%d %H:%M') if administrativos.salida_admin1 else '',
                administrativos.entrada_admin2.strftime('%Y-%m-%d %H:%M') if administrativos.entrada_admin2 else '',
                administrativos.salida_admin2.strftime('%Y-%m-%d %H:%M') if administrativos.salida_admin2 else '',
            ]

            update_excel(datos_vehiculo_admin, "Administrativos")
            return redirect('listar_vehiculos_admin_pendientes')
        except RegistroAdministrativos.DoesNotExist:
            return HttpResponse("Error: admin no encontrado.", status=404)
    return HttpResponse("Error al procesar la entrada 2.", status=500)


# Función para registrar salida 2 del administrativo
def registrar_salida_admin2(request, id):
    if request.method == 'POST':
        try:
            administrativos = RegistroAdministrativos.objects.get(id=id)
            # Registrar la salida con la fecha y hora actual convertida a naive (sin tzinfo)
            salida_admin2 =datetime.now()

            administrativos.salida_admin2 = salida_admin2  # Guardar fecha naive
            administrativos.save()

            datos_vehiculo_admin = [
                administrativos.id,
                administrativos.entrada_admin1.strftime('%Y-%m-%d %H:%M') if administrativos.entrada_admin1 else '',
                administrativos.vehiculo or '',
                administrativos.patente or '',
                administrativos.apellido_nombre_admin or '',
                administrativos.observaciones or '',
                administrativos.salida_admin1.strftime('%Y-%m-%d %H:%M') if administrativos.salida_admin1 else '',
                administrativos.entrada_admin2.strftime('%Y-%m-%d %H:%M') if administrativos.entrada_admin2 else '',
                administrativos.salida_admin2.strftime('%Y-%m-%d %H:%M') if administrativos.salida_admin2 else '',
            ]

            update_excel(datos_vehiculo_admin, "Administrativos")
            return redirect('listar_vehiculos_admin_pendientes')
        except RegistroAdministrativos.DoesNotExist:
            return HttpResponse("Error: admin no encontrado.", status=404)
    return HttpResponse("Error al procesar la salida 2.", status=500)

def registrar_salida_camion(request, id):
    if request.method == 'POST':
        try:
            camion = RegistroCamiones.objects.get(id=id)
            # Registrar la salida con la fecha y hora actual convertida a naive (sin tzinfo)
            egreso = datetime.now()

            camion.egreso = egreso  # Guardar fecha naive
            camion.save()

            datos_camion = [
                camion.id,
                camion.chofer or '',
                camion.dni or '',
                camion.tractor or '',
                camion.semi or '',
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.transporte,
                camion.egreso.strftime('%Y-%m-%d %H:%M') if camion.egreso else '',
                camion.ingreso2 or '',
                camion.egreso2 or '',
                camion.ingreso3 or '',
                camion.egreso3 or '',
            ]

            update_excel(datos_camion, "Camiones")
            return redirect('listar_camiones_pendientes')
        except RegistroCamiones.DoesNotExist:
            return HttpResponse("Error: Camión no encontrado.", status=404)

    return HttpResponse("Error al procesar la salida.", status=500)

def registrar_salida_camion2(request, id):
    if request.method == 'POST':
        try:
            camion = RegistroCamiones.objects.get(id=id)

            # Obtener el valor de ingreso2 desde el formulario
            egreso2 = request.POST.get('egreso2', None)

            if not egreso2:
                return HttpResponse("Error: El campo 'egreso2' es obligatorio.", status=400)

            # Asignar el valor de texto al campo ingreso2
            camion.egreso2 = egreso2
            camion.save()

            datos_camion = [
                camion.id,
                camion.chofer or '',
                camion.dni or '',
                camion.tractor or '',
                camion.semi or '',
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.transporte or '',
                camion.egreso.strftime('%Y-%m-%d %H:%M') if camion.egreso else '',
                camion.ingreso2 or '',
                camion.egreso2 or '',
                camion.ingreso3 or '',
                camion.egreso3 or '',
            ]

            update_excel(datos_camion, "Camiones")
            return redirect('listar_camiones_pendientes')

        except RegistroCamiones.DoesNotExist:
            return HttpResponse("Error: Camión no encontrado.", status=404)

    return HttpResponse("Error al procesar el registro de egreso2.", status=500)

def registrar_salida_camion3(request, id):
    if request.method == 'POST':
        try:
            camion = RegistroCamiones.objects.get(id=id)

            # Obtener el valor de ingreso2 desde el formulario
            egreso3 = request.POST.get('egreso3', None)

            if not egreso3:
                return HttpResponse("Error: El campo 'egreso3' es obligatorio.", status=400)

            # Asignar el valor de texto al campo ingreso2
            camion.egreso3 = egreso3
            camion.save()

            datos_camion = [
                camion.id,
                camion.chofer or '',
                camion.dni or '',
                camion.tractor or '',
                camion.semi or '',
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.transporte or '',
                camion.egreso.strftime('%Y-%m-%d %H:%M') if camion.egreso else '',
                camion.ingreso2 or '',
                camion.egreso2 or '',
                camion.ingreso3 or '',
                camion.egreso3 or '',
            ]

            update_excel(datos_camion, "Camiones")
            return redirect('listar_camiones_pendientes')

        except RegistroCamiones.DoesNotExist:
            return HttpResponse("Error: Camión no encontrado.", status=404)

    return HttpResponse("Error al procesar el registro de egreso3.", status=500)

def registrar_ingreso_camion2(request, id):
    if request.method == 'POST':
        try:
            camion = RegistroCamiones.objects.get(id=id)

            # Obtener el valor de ingreso2 desde el formulario
            ingreso2 = request.POST.get('ingreso2', None)

            if not ingreso2:
                return HttpResponse("Error: El campo 'ingreso2' es obligatorio.", status=400)

            # Asignar el valor de texto al campo ingreso2
            camion.ingreso2 = ingreso2
            camion.save()

            datos_camion = [
                camion.id,
                camion.chofer or '',
                camion.dni or '',
                camion.tractor or '',
                camion.semi or '',
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.transporte or '',
                camion.egreso.strftime('%Y-%m-%d %H:%M') if camion.egreso else '',
                camion.ingreso2 or '',
                camion.egreso2 or '',
                camion.ingreso3 or '',
                camion.egreso3 or '',
            ]

            update_excel(datos_camion, "Camiones")
            return redirect('listar_camiones_pendientes')

        except RegistroCamiones.DoesNotExist:
            return HttpResponse("Error: Camión no encontrado.", status=404)

    return HttpResponse("Error al procesar el registro de ingreso2.", status=500)

def registrar_ingreso_camion3(request, id):
    if request.method == 'POST':
        try:
            camion = RegistroCamiones.objects.get(id=id)

            ingreso3 = request.POST.get('ingreso3', None)

            if not ingreso3:
                return HttpResponse("Error: El campo 'ingreso3' es obligatorio.", status=400)

            # Asignar el valor de texto al campo ingreso2
            camion.ingreso3 = ingreso3
            camion.save()

            datos_camion = [
                camion.id,
                camion.chofer or '',
                camion.dni or '',
                camion.tractor or '',
                camion.semi or '',
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.transporte or '',
                camion.egreso.strftime('%Y-%m-%d %H:%M') if camion.egreso else '',
                camion.ingreso2 or '',
                camion.egreso2 or '',
                camion.ingreso3 or '',
                camion.egreso3 or '',
            ]

            update_excel(datos_camion, "Camiones")
            return redirect('listar_camiones_pendientes')

        except RegistroCamiones.DoesNotExist:
            return HttpResponse("Error: Camión no encontrado.", status=404)

    return HttpResponse("Error al procesar el registro de ingreso3.", status=500)

# Exportar todos los registros a Excel
def exportar_todos_a_excel(request):
    try:
        # Exportar registros de vehículos
        print("Exportando registros de vehículos...")
        vehiculos = RegistroVehiculo.objects.all()
        for vehiculo in vehiculos:
            datos_vehiculo = [
                vehiculo.entrada.strftime('%Y-%m-%d %H:%M') if vehiculo.entrada else '',
                vehiculo.dni or '',
                vehiculo.pte_numero or '',
                vehiculo.apellido_nombre or '',
                vehiculo.empresa or '',
                vehiculo.ingreso_remitos or ''
            ]
            print(f"Datos de Vehículo a exportar: {datos_vehiculo}")
            update_excel(datos_vehiculo, "Vehiculos")

        # Exportar registros de camiones
        print("Exportando registros de camiones...")
        camiones = RegistroCamiones.objects.all()
        for camion in camiones:
            datos_camion = [
                camion.ingreso.strftime('%Y-%m-%d %H:%M') if camion.ingreso else '',
                camion.chofer or '',
                camion.dni or '',
                camion.transporte or '',
                camion.tractor or '',
                camion.semi or ''
            ]
            print(f"Datos de Camión a exportar: {datos_camion}")
            update_excel(datos_camion, "Camiones")

        # Exportar registros administrativos
        print("Exportando registros administrativos...")
        administrativos = RegistroAdministrativos.objects.all()
        for admin in administrativos:
            datos_admin = [
                admin.entrada_admin1.strftime('%Y-%m-%d %H:%M') if admin.entrada_admin1 else '',
                admin.salida_admin1.strftime('%Y-%m-%d %H:%M') if admin.salida_admin1 else '',
                admin.vehiculo or '',
                admin.patente or '',
                admin.apellido_nombre_admin or '',
                admin.observaciones or ''
            ]
            print(f"Datos Administrativos a exportar: {datos_admin}")
            update_excel(datos_admin, "Administrativos")

        return HttpResponse("Todos los registros han sido exportados exitosamente a Google Drive.")

    except Exception as e:
        print(f"Error al exportar los registros: {e}")
        return HttpResponse(f"Error al exportar los registros: {e}")
def listar_vehiculos_pendientes(request):
    try:
        vehiculos_pendientes = RegistroVehiculo.objects.filter(
            Q(salida_vehiculo__isnull=True) | Q(egreso_remitos__isnull=True)
        )

        return render(request, 'registro/Control de Ingreso y Egreso de Vehículos.html', {
            'vehiculos_pendientes': vehiculos_pendientes
        })
    except Exception as e:
        print(f"Error al obtener los vehículos pendientes: {e}")
        return render(request, 'registro/Control de Ingreso y Egreso de Vehículos.html', {
            'vehiculos_pendientes': []
        })

def listar_vehiculos_admin_pendientes(request):
    vehiculos_admin_pendientes = RegistroAdministrativos.objects.filter(
        Q(salida_admin1__isnull=True) | Q(salida_admin2__isnull=True) | Q(entrada_admin2__isnull=True)
    )
    print(vehiculos_admin_pendientes)  # Esto imprimirá la lista de objetos en la consola
    return render(request, 'registro/Administrativos de Softys.html', {
        'vehiculos_admin_pendientes': vehiculos_admin_pendientes  # Cambiar el nombre para que coincida con el template
    })


def listar_camiones_pendientes(request):
    try:
        camiones_pendientes = RegistroCamiones.objects.filter(
            Q(ingreso2__isnull=True) | Q(ingreso3__isnull=True) | Q(egreso__isnull=True) | Q(egreso2__isnull=True)| Q(egreso3__isnull=True)
        )
        return render(request, 'registro/Control de Camiones.html', {
           'camiones_pendientes': camiones_pendientes  # Variable que usará el template
        })
    except Exception as e:
        print(f"Error al obtener los camiones pendientes: {e}")
        return render(request, 'registro/Control de Camiones.html', {
            'camiones_pendientes': []
            })
            