# Generated by Django 4.2.5 on 2023-10-23 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0006_alter_nueva_propuesta_vigencia_certificado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nueva_propuesta',
            name='vigencia_certificado',
        ),
    ]
