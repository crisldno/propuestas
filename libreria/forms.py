from django import forms

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
#     (15,"Persona Natural Para Actividad Comercial (Rut)"), 
# )

class Formulario_propuesta(forms.Form):
    tipo_documento = forms.CharField(max_length=100, required=True)
    numero_documento = forms.CharField(max_length=150, required=True)
    razon_social_o_nombre = forms.CharField(max_length=200, required=True)
    correo_electronico = forms.EmailField(max_length=150, required=True)
    plataforma = forms.CharField(max_length=50, required=True)
    tipo_certificado = forms.CharField(max_length=100,required=True)
    formato_entrega = forms.CharField(max_length=100, required=True)
    cupon_descuento = forms.CharField(max_length=50, required=False)
    