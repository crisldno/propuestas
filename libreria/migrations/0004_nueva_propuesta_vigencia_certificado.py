# Generated by Django 4.2.5 on 2023-10-19 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0003_remove_nueva_propuesta_nombre_asesor_contact_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='nueva_propuesta',
            name='vigencia_certificado',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
