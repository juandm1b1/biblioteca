# Generated by Django 3.1.3 on 2020-12-10 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_auto_20201210_1149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'permissions': [('permiso_desde_codigo', 'Permiso creado desde el código')]},
        ),
    ]
