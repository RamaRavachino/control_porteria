# Generated by Django 5.1.3 on 2024-12-12 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0011_alter_registroadministrativos_entrada_admin1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroadministrativos',
            name='entrada_admin1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='entrada_admin2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='salida_admin1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='salida_admin2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='ingreso_camion1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='ingreso_camion2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='ingreso_camion3',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='salida_camion1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='salida_camion2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='salida_camion3',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrovehiculo',
            name='entrada',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrovehiculo',
            name='fecha_salida',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrovehiculo',
            name='ingreso_remitos',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrovehiculo',
            name='salida_vehiculo',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]