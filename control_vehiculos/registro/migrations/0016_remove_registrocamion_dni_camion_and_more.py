# Generated by Django 5.1.3 on 2024-12-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0015_alter_registrovehiculo_dni_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrocamion',
            name='dni_camion',
        ),
        migrations.RemoveField(
            model_name='registrocamion',
            name='ingreso_camion1',
        ),
        migrations.RemoveField(
            model_name='registrocamion',
            name='ingreso_camion2',
        ),
        migrations.RemoveField(
            model_name='registrocamion',
            name='ingreso_camion3',
        ),
        migrations.RemoveField(
            model_name='registrocamion',
            name='salida_camion1',
        ),
        migrations.RemoveField(
            model_name='registrocamion',
            name='salida_camion2',
        ),
        migrations.RemoveField(
            model_name='registrocamion',
            name='salida_camion3',
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='dni',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='egreso',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='egreso2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='egreso3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='ingreso',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='ingreso2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrocamion',
            name='ingreso3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='chofer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='semi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='tractor',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamion',
            name='transporte',
            field=models.TextField(blank=True, null=True),
        ),
    ]
