# Generated by Django 5.1.3 on 2024-12-11 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0006_registroadministrativos_entrada_admin2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrocamion',
            name='ingreso',
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='ingreso_camion1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='ingreso_camion2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='ingreso_camion3',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='salida_camion1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='salida_camion2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='salida_camion3',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
