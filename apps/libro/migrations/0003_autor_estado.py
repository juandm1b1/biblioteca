# Generated by Django 2.0 on 2020-11-23 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0002_auto_20201122_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='autor',
            name='estado',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
    ]
