# Generated by Django 5.1.3 on 2025-01-12 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0024_dummy_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroadministrativos',
            name='apellido_nombre_admin',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='entrada_admin1',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='observaciones',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='patente',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registroadministrativos',
            name='vehiculo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
