import os
import django
from django.db.models import Q
import sys

# Añadir el directorio del proyecto a sys.path
# Asegúrate de que el path sea el directorio donde reside settings.py
project_path = 'C:/Users/ramiro_ravachino/Desktop/djangoproject/control_vehiculos'
sys.path.append(project_path)

# Especificar la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_vehiculos.settings')

# Configurar Django
django.setup()

# Ahora puedes importar y usar tus modelos Django
from registro.models import RegistroCamiones

# Asegúrate de reemplazar 'control_vehiculos.settings' con el path correcto de tus settings si es necesario
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control_vehiculos.settings")

def probar_consulta_camiones():
    try:
        camiones_pendientes = RegistroCamiones.objects.filter(
            Q(ingreso2__isnull=True) | Q(ingreso3__isnull=True) |
            Q(egreso__isnull=True) | Q(egreso2__isnull=True) | Q(egreso3__isnull=True)
        )
        print("Número de camiones pendientes: ", len(camiones_pendientes))
        for camion in camiones_pendientes:
            print("ID:", camion.id, "Chofer:", camion.chofer, "DNI:", camion.dni,
                  "Tractor:", camion.tractor, "Semi:", camion.semi, "Transporte:", camion.transporte)
            print("Ingreso:", camion.ingreso, "Egreso:", camion.egreso, "Ingreso2:", camion.ingreso2,
                  "Egreso2:", camion.egreso2, "Ingreso3:", camion.ingreso3, "Egreso3:", camion.egreso3)
    except Exception as e:
        print("Error al obtener los camiones pendientes: ", e)

if __name__ == "__main__":
    probar_consulta_camiones()
