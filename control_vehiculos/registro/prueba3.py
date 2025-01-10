from google_drive_utils import leer_datos_excel

datos = leer_datos_excel("Vehiculos")
print("Datos del Excel:", datos)

from google_drive_utils import leer_datos_excel

def listar_vehiculos_pendientes():
    try:
        # Leer los datos desde el Excel
        vehiculos_pendientes = leer_datos_excel("Vehiculos")

        # Filtrar los vehículos sin salida registrada
        vehiculos_pendientes = [
            vehiculo for vehiculo in vehiculos_pendientes if not vehiculo.get('Salida')
        ]

        print("Vehículos pendientes:")
        for vehiculo in vehiculos_pendientes:
            print(vehiculo)

    except Exception as e:
        print(f"Error al leer los vehículos pendientes: {e}")

# Llamar a la función para probarla
if __name__ == "__main__":
    listar_vehiculos_pendientes()
