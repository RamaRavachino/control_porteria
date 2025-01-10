# Generated by Django 5.1.3 on 2024-12-12 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0012_alter_registroadministrativos_entrada_admin1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroadministrativos',
            name='apellido_nombre_admin',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='patente',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='dni_camion',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='transporte',
            field=models.CharField(max_length=100),
        ),
    ]