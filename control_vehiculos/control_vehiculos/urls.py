from django.contrib import admin
from django.urls import path, include
from autenticacion import views as auth_views  # Importar la vista de autenticación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.login_view, name='login'), 
    path('pagina_principal/', include('registro.urls')),  
    path('auth/', include('autenticacion.urls')),  
]
