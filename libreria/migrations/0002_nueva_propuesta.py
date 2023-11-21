# Generated by Django 4.2.5 on 2023-10-03 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='nueva_propuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(max_length=100)),
                ('numero_documento', models.CharField(max_length=150)),
                ('razon_social_o_nombre', models.CharField(max_length=200)),
                ('correo_electronico', models.EmailField(max_length=150)),
                ('nombre_asesor_contact_center', models.CharField(max_length=100)),
                ('plataforma', models.CharField(max_length=50)),
                ('tipo_certificado', models.CharField(max_length=100)),
                ('formato_entrega', models.CharField(max_length=100)),
                ('cupon_descuento', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]