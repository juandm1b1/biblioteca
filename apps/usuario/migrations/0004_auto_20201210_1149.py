# Generated by Django 3.1.3 on 2020-12-10 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20201210_1002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_activo',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_administrador',
            new_name='is_staff',
        ),
    ]
