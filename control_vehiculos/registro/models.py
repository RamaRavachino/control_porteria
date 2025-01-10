from django.db import models

class RegistroVehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    entrada = models.DateTimeField()
    dni = models.CharField(max_length=20)
    pte_numero = models.CharField(max_length=20, null=True, blank=True)
    apellido_nombre = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.CharField(max_length=255, null=True, blank=True)
    ingreso_remitos = models.CharField(max_length=255, null=True, blank=True)
    egreso_remitos = models.CharField(max_length=255, null=True, blank=True)  
    salida_vehiculo = models.DateTimeField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Vehículo {self.id} - DNI {self.dni}"


"""class RegistroCamiones(models.Model):
    id = models.AutoField(primary_key=True)
    chofer = models.CharField(max_length=50, null=True, blank=True)
    dni = models.CharField(max_length=50, null=True, blank=True)
    tractor = models.CharField(max_length=50, null=True, blank=True)
    semi = models.CharField(max_length=50, null=True, blank=True)
    ingreso = models.DateTimeField(null=True, blank=True)
    egreso = models.DateTimeField(null=True, blank=True)
    transporte = models.CharField(max_length=50, null=True, blank=True)
    ingreso2 = models.CharField(max_length=50, null=True, blank=True)
    ingreso3 = models.CharField(max_length=50, null=True, blank=True)
    egreso2 = models.CharField(max_length=50, null=True, blank=True)
    egreso3 = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.transporte} - {self.tractor}" """

from django.db import models
from django.utils.timezone import make_aware
import pytz

from django.db import models

class RegistroCamiones(models.Model):
    id = models.AutoField(primary_key=True)  # Campo autoincremental
    chofer = models.CharField(max_length=50, null=True, blank=True)
    dni = models.CharField(max_length=50, null=True, blank=True)
    tractor = models.CharField(max_length=50, null=True, blank=True)
    semi = models.CharField(max_length=50, null=True, blank=True)
    ingreso = models.DateTimeField()
    egreso = models.DateTimeField(null=True, blank=True)
    ingreso2 = models.CharField(max_length=50, null=True, blank=True)
    egreso2 = models.CharField(max_length=50, null=True, blank=True) 
    ingreso3 = models.CharField(max_length=50, null=True, blank=True)
    egreso3 = models.CharField(max_length=50, null=True, blank=True)
    transporte = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        # No convertir a timezone-aware. Trabajar solo con naive.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Camión {self.chofer} - {self.tractor}"




class RegistroAdministrativos(models.Model):
    id = models.AutoField(primary_key=True)
    entrada_admin1 = models.DateTimeField()
    salida_admin1 = models.DateTimeField(blank=True, null=True)
    vehiculo = models.CharField(max_length=50, null=True, blank=True)
    patente = models.CharField(max_length=50, null=True, blank=True) 
    apellido_nombre_admin = models.CharField(max_length=50, null=True, blank=True)
    observaciones = models.TextField(max_length=50, null=True, blank=True)
    salida_admin2 = models.DateTimeField(blank=True, null=True)
    entrada_admin2 = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.apellido_nombre_admin} - {self.vehiculo}"
