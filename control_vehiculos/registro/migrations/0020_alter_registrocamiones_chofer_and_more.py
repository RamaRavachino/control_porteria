# Generated by Django 5.1.3 on 2025-01-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0019_alter_registrocamiones_egreso2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocamiones',
            name='chofer',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='dni',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='egreso2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='egreso3',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='ingreso2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='ingreso3',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='semi',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='tractor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registrocamiones',
            name='transporte',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
