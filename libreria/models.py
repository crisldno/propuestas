from django.db import models
from django.utils import timezone


# Modelo Usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)

    def _str_(self):
        return self.nombre

# Modelo Cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=20)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    def _str_(self):
        return self.nombre

# Modelo Producto
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    formato_entrega = models.CharField(max_length=50)
    vigencia = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_descuento = models.CharField(max_length=20)

    def _str_(self):
        return self.nombre

# Modelo Propuesta
class Propuesta(models.Model):
    id_propuesta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_asesor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plataforma = models.CharField(max_length=50)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def _str_(self):
        return f'Propuesta para {self.id_cliente}'

# Modelo Permisos
class Permisos(models.Model):
    generar_propuesta = models.BooleanField(default=False)
    ver_historial = models.BooleanField(default=False)
    descargar_en_pdf = models.BooleanField(default=False)
    crear_usuario = models.BooleanField(default=False)

# Modelo Roles
class Roles(models.Model):
    asesor = models.BooleanField(default=False)
    cliente = models.BooleanField(default=False)
    admin_contact_center = models.BooleanField(default=False)
    back_office = models.BooleanField(default=False)


# Modelo Nueva Propuesta
class nueva_propuesta(models.Model):
    tipo_documento = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=150)
    razon_social_o_nombre = models.CharField(max_length=200)
    correo_electronico = models.EmailField(max_length=150)
    plataforma = models.CharField(max_length=50)
    # TIPO_CERTIFICADO_CHOICES = (
    #     (10, "Facturación Electrónica - Persona Jurídica"),
    #     (11, "Facturación Electrónica - Persona Natural"),
    #     (6,"Comunidad Académica"),
    #     (9,"Pertenencia Empresa"),
    #     (7,"Profesional Titulado"),
    #     (8,"Representante Legal"),
    #     (12," Función Púbica"),
    #     (13,"Persona Jurídica"),
    #     (14,"Función Publica para SIIF Nación"),
    #     (5,"Persona Natural"),
    #     (15,"Persona Natural Para Actividad Comercial (Rut)"),)
    tipo_certificado = models.CharField(max_length=100)
    formato_entrega = models.CharField(max_length=100)
    cupon_descuento = models.CharField(max_length=50, blank=True, null=True)
    precio_1 = models.CharField(max_length=50, blank=True, null=True)
    precio_2 = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    asesor = models.CharField(max_length=200)



    def _str_(self):
        return self.razon_social_o_nombre