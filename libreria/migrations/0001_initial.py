# Generated by Django 4.2.5 on 2023-10-03 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('tipo_documento', models.CharField(max_length=20)),
                ('numero_documento', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Permisos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generar_propuesta', models.BooleanField(default=False)),
                ('ver_historial', models.BooleanField(default=False)),
                ('descargar_en_pdf', models.BooleanField(default=False)),
                ('crear_usuario', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('formato_entrega', models.CharField(max_length=50)),
                ('vigencia', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('codigo_descuento', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asesor', models.BooleanField(default=False)),
                ('cliente', models.BooleanField(default=False)),
                ('admin_contact_center', models.BooleanField(default=False)),
                ('back_office', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('numero_documento', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Propuesta',
            fields=[
                ('id_propuesta', models.AutoField(primary_key=True, serialize=False)),
                ('plataforma', models.CharField(max_length=50)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id_asesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.usuario')),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.cliente')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.producto')),
            ],
        ),
    ]
