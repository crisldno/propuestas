from django.core.mail import send_mail
from django.template.loader import render_to_string

def generar_informe(propuesta):
    informe_data = {
        'tipo_documento': propuesta.tipo_documento,
        'numero_documento': propuesta.numero_documento,
        'razon_social_o_nombre': propuesta.razon_social_o_nombre,
        'correo_electronico': propuesta.correo_electronico,
        'plataforma': propuesta.plataforma,
        'tipo_certificado': propuesta.tipo_certificado,
        'formato_entrega': propuesta.formato_entrega,
        'cupon_descuento': propuesta.cupon_descuento
    }
    
    # Agregar declaraciones de impresión para verificar los datos
    print("Datos del informe generados:")
    for clave, valor in informe_data.items():
        print(f"{clave}: {valor}")
    
    
     # Envío de correo electrónico
    subject = 'Propuesta Comercial ' +  propuesta.razon_social_o_nombre
    message = 'El servicio de notificación de alertas de Andes SCD le informa la creación de su propuesta comercial:\n\n'
    for clave, valor in informe_data.items():
        message += f"{clave}: {valor}\n"

    from_email = 'raandesscd@gmail.com'
    recipient_list = [propuesta.correo_electronico , 'eldaniedoc@gmail.com']

 

    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"Correo enviado a {propuesta.correo_electronico}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


    return informe_data