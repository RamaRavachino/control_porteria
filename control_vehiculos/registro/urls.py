from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.pagina_principal, name='pagina_principal'),
    
    # Camiones
    path('camiones/pendientes/', views.listar_camiones_pendientes, name='listar_camiones_pendientes'),
    path('camiones/registrar/', views.control_camiones, name='control_camiones'),
    path('registrar-salida-camion1/<int:id>/', views.registrar_salida_camion, name='registrar_salida_camion'),
    path('registrar-salida-camion2/<int:id>/', views.registrar_salida_camion2, name='registrar_salida_camion2'),
    path('registrar-salida-camion3/<int:id>/', views.registrar_salida_camion3, name='registrar_salida_camion3'),
    path('registrar-ingreso-camion2/<int:id>/', views.registrar_ingreso_camion2, name='registrar_ingreso_camion2'),
    path('registrar-ingreso-camion3/<int:id>/', views.registrar_ingreso_camion3, name='registrar_ingreso_camion3'),

    # Vehículos
    path('vehiculos/registrar/', views.control_vehiculos, name='control_vehiculos'),
    path('vehiculos/pendientes/', views.listar_vehiculos_pendientes, name='listar_vehiculos_pendientes'),
    path('registrar-remitos/<int:id>/', views.registrar_remitos, name='registrar_remitos'),
    path('registrar-salida/<int:id>/', views.registrar_salida, name='registrar_salida'),

    # Administrativos
    path('administrativos/registrar/', views.control_administrativos, name='control_administrativos'),  # Registro de administrativos
    path('administrativos/pendientes/', views.listar_vehiculos_admin_pendientes, name='listar_vehiculos_admin_pendientes'),
    path('registrar-salida-admin/<int:id>/', views.registrar_salida_admin, name='registrar_salida_admin'),  # Salida 1
    path('registrar-entrada-admin2/<int:id>/', views.registrar_entrada_admin2, name='registrar_entrada_admin2'),  # Entrada 2
    path('registrar-salida-admin2/<int:id>/', views.registrar_salida_admin2, name='registrar_salida_admin2'),  # Salida 2

    # Exportación a Excel
    path('exportar/', views.exportar_todos_a_excel, name='exportar_todos'),
]
