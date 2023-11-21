import requests
import json
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView 
from .models import nueva_propuesta
from .forms import Formulario_propuesta
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from bs4 import BeautifulSoup
from .utils import generar_informe
from django.http import Http404
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa as pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import pandas as pd
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




class Logueo(LoginView):
    template_name = "oferta/login.html"
    field = '_all_'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('oferta')

def inicio(request):
    return render(request, 'oferta/inicio.html')

def is_superuser(user):
    return user.is_superuser


@login_required
def oferta(request):
    if request.user.is_superuser:
        # Si es un superusuario, muestra todas las propuestas
        propuestas = nueva_propuesta.objects.all()
    else:
        # Si no es un superusuario, filtra las propuestas por el usuario actual
        propuestas = nueva_propuesta.objects.filter(asesor=request.user)

    query = request.GET.get('area-buscar')

    if query:
        propuestas = propuestas.filter(
            Q(razon_social_o_nombre__icontains=query) | Q(numero_documento__icontains=query)
        )

    return render(request, 'oferta/index.html', {'propuestas': propuestas})




def crear(request):
    return render(request, 'oferta/crear.html')

def editar(request):
    return render(request, 'oferta/editar.html')



def lista_propuestas(request):
    propuestas_lista = nueva_propuesta.objects.all()

    # Número de propuestas por página
    propuestas_por_pagina = 10

    paginator = Paginator(propuestas_lista, propuestas_por_pagina)
    pagina = request.GET.get('pagina')

    try:
        nueva_propuesta = paginator.page(pagina)
    except PageNotAnInteger:
        # Si la página no es un entero, muestra la primera página.
        nueva_propuesta = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima de la última página), muestra la última página.
        nueva_propuesta = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'propuestas': nueva_propuesta})







def crear_propuesta(request):

   
    if request.method == 'POST':
        form = Formulario_propuesta(request.POST)



        if form.is_valid():
            tipo_documento = form.cleaned_data['tipo_documento']
            numero_documento = form.cleaned_data['numero_documento']
            razon_social_o_nombre = form.cleaned_data['razon_social_o_nombre']

            # Verificar si ya existe una propuesta con el mismo número de documento o nombre/razón social
            propuesta_existente = nueva_propuesta.objects.filter(
                numero_documento=numero_documento,
                razon_social_o_nombre=razon_social_o_nombre
            ).exists()
            
            if propuesta_existente:
            # Mostrar una alerta al usuario
                return render(request, 'alerta.html', {'mensaje': 'Ya existe una propuesta con el mismo número de documento o nombre/razón social.'})
        
        
            correo_electronico = form.cleaned_data['correo_electronico']
            plataforma = form.cleaned_data['plataforma']
            tipo_certificado = form.cleaned_data['tipo_certificado']
            formato_entrega = form.cleaned_data['formato_entrega']
            cupon_descuento = form.cleaned_data.get('cupon_descuento', None)  

            

            url = "https://build.andesscd.com.co/ApiRest/public/api/getDiscount"
            headers = {
                    'Content-Type': 'application/json',
                    'api-key': 'a9b7f861-d9a3-4c1b-80e7-1297bcea3bbe',
                    'Cookie': 'lumen_session=TgnA64AK7M0RpDG0Wx0vzFYxjAPmxttX2tBKWgvt'
    }

            payload_id_3 = json.dumps({
                "id_vigencia": "3",
                "id_tipocertificado": tipo_certificado,
                "id_formaentregacertificado":"4" ,
                "con_token": False,
                "tipo_documento": 2,
                "id_documento": numero_documento,
                "cupon": cupon_descuento
            })

            response_id_3 = requests.post(url, headers=headers, data=payload_id_3)
            response_data_id_3 = None

            if response_id_3.status_code == 200:
                response_data_id_3 = response_id_3.json()

            
            print(response_data_id_3)
            
            payload_id_4 = json.dumps({
                "id_vigencia": "4",
                "id_tipocertificado": tipo_certificado,
                "id_formaentregacertificado": "4",
                "con_token": False,
                "tipo_documento": 2,    
                "id_documento": numero_documento,
                "cupon": cupon_descuento
            })

            response_id_4 = requests.post(url, headers=headers, data=payload_id_4)
            response_data_id_4 = None

            if response_id_4.status_code == 200:
                response_data_id_4 = response_id_4.json()
            print("Valor de response_data_id_4:", response_data_id_4)
            print("Respuesta de la API:", response_data_id_3,response_data_id_4)
            print("Datos enviados en la solicitud:", payload_id_3,payload_id_4)

            # Ahora, extrae los datos relevantes de la respuesta
            precio3 = response_data_id_3.get("precio", "No disponible")
            precio4 = response_data_id_4.get("precio", "No disponible")

            porcentaje_impuesto = response_data_id_3.get("porcentaje_impuesto", "No disponible")
            
            total_pagar3 = response_data_id_3.get("total_pagar", "No disponible")
            total_pagar4 = response_data_id_4.get("total_pagar", "No disponible")
           
            # Asegúrate de que los datos se han extraído correctamente
            print("Precio:", precio3,precio4)
            print("Porcentaje de Impuesto:", porcentaje_impuesto)
            print("Total a Pagar:", total_pagar3,total_pagar4)
            """
            mapeo_tipo_certificado = {
                "10": "Facturación Electrónica - Persona Jurídica",
                "11": "Facturación Electrónica - Persona Natural",
                "6": "Comunidad Académica",
                "9": "Pertenencia Empresa",
                "7": "Profesional Titulado",
                "8": "Representante Legal",
                "12": "Función Pública",
                "13": "Persona Jurídica",
                "14": "Función Pública para SIIF Nación",
                "5": "Persona Natural",
                "15": "Persona Natural Para Actividad Comercial (Rut)"
            }


            valor_seleccionado = request.POST['tipo_certificado']
            tipo_certificado = mapeo_tipo_certificado.get(valor_seleccionado, '')
            """
            nueva_propuesta_obj = nueva_propuesta(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                razon_social_o_nombre=razon_social_o_nombre,
                correo_electronico=correo_electronico,
                plataforma=plataforma,
                tipo_certificado=tipo_certificado,
                formato_entrega=formato_entrega,
                cupon_descuento=cupon_descuento,
                precio_1=precio3,  
                precio_2=precio4,
                asesor=request.user,
                
            )

            #
            
            nueva_propuesta_obj.save()
            
            informe_data = generar_informe(nueva_propuesta_obj)
            
            return render(request, 'oferta/confirmacion.html', {'informe_data': informe_data,'response_data_id_3': response_data_id_3, 'response_data_id_4': response_data_id_4})

        return redirect('confirmacion')
    
        

    else:
        form = Formulario_propuesta()

    return render(request, 'oferta/crear.html', {'form': form})


def enviar_propuesta(request,propuesta_id):
    propuesta_id = get_object_or_404(nueva_propuesta, id=propuesta_id)
    
    
    nueva_propuesta.enviada = True
    nueva_propuesta.save()
    
    
    return render(request, 'confirmacion.html')


def confirmacion(request):
    return render(request, 'oferta/informe.html')




def descargar_excel(request):
    filter = request.GET.get('filter', None)

    if filter == 'ultimo':
        # Filtra propuestas creadas en el último mes
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    elif filter == 'ultimos_dos':
        # Filtra propuestas creadas en los últimos dos meses
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)
    elif filter == 'ultimos_tres':
        # Filtra propuestas creadas en los últimos tres meses
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)

    elif filter == 'por_defecto':
        # Filtra propuestas creadas en los últimos seis meses
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
    else:
        
        start_date = datetime(1970, 1, 1)
        end_date = datetime.now()

    if request.user.is_superuser:
        proposals = nueva_propuesta.objects.filter(fecha_creacion__range=(start_date, end_date))
    else:
        proposals = nueva_propuesta.objects.filter(asesor=request.user, fecha_creacion__range=(start_date, end_date))
    
    
    data = {
        'Número Propuesta': [propuesta.id for propuesta in proposals],
        'tipo documento': [propuesta.tipo_documento for propuesta in proposals],
        'numero documento': [propuesta.numero_documento for propuesta in proposals],
        'razon social/nombre': [propuesta.razon_social_o_nombre for propuesta in proposals],
        'correo electronico': [propuesta.correo_electronico for propuesta in proposals],
        'plataforma': [propuesta.plataforma for propuesta in proposals],
        'tipo certificado': [propuesta.tipo_certificado for propuesta in proposals],
        'formato entrega': [propuesta.formato_entrega for propuesta in proposals],
        'cupon descuento': [propuesta.cupon_descuento for propuesta in proposals],
        'Precio 1': [propuesta.precio_1 for propuesta in proposals],
        'Precio 2': [propuesta.precio_2 for propuesta in proposals],
        'asesor': [propuesta.asesor for propuesta in proposals],
        

        



    }
   
    df = pd.DataFrame(data)
    
    
    output = BytesIO()
    excel_writer = pd.ExcelWriter(output, engine='xlsxwriter')

    
    df.to_excel(excel_writer, sheet_name='Propuestas', index=False)

    
    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Propuestas']

    
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#0B2057', 
        'font_size': 14,  
        'text_wrap': True,
        'border': 1 ,
        'font_color': 'white'
    })

    #Encabezados
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        
        worksheet.set_row(0, 30)  

    
    cell_format = workbook.add_format({
        'text_wrap': True,
        'border': 1  
    })

    for row_num in range(1, len(proposals) + 1):
        for col_num, value in enumerate(df.iloc[row_num - 1]):
            worksheet.write(row_num, col_num, value, cell_format)

    
    worksheet.set_column(0, len(df.columns) - 1, 20)

    
    excel_writer.close()

    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=propuestas.xlsx'
    response.write(output.getvalue())

    return response

def informe(request, propuesta_id):
    
    try:
    
        propuesta = nueva_propuesta.objects.get(id=propuesta_id)
        
        tipo_certificado = propuesta.tipo_certificado
        cupon_descuento = propuesta.cupon_descuento
        numero_documento = propuesta.numero_documento
    except nueva_propuesta.DoesNotExist:
    
        return render(request, 'oferta/informe.html', {'informe_data': None})
    
    

    url = "https://build.andesscd.com.co/ApiRest/public/api/getDiscount"
    headers = {
                'Content-Type': 'application/json',
                'api-key': 'a9b7f861-d9a3-4c1b-80e7-1297bcea3bbe',
                'Cookie': 'lumen_session=TgnA64AK7M0RpDG0Wx0vzFYxjAPmxttX2tBKWgvt'
    }

    payload_id_3 = json.dumps({
        "id_vigencia": "3",
        "id_tipocertificado": tipo_certificado,
        "id_formaentregacertificado":"4" ,
        "con_token": False,
        "tipo_documento": 2,
        "id_documento": numero_documento,
        "cupon": cupon_descuento
    })

    response_id_3 = requests.post(url, headers=headers, data=payload_id_3)
    response_data_id_3 = None

    if response_id_3.status_code == 200:
        response_data_id_3 = response_id_3.json()

            
    print(response_data_id_3)
            
    payload_id_4 = json.dumps({
        "id_vigencia": "4",
        "id_tipocertificado": tipo_certificado,
        "id_formaentregacertificado": "4",
        "con_token": False,
        "tipo_documento": 2,    
        "id_documento": numero_documento,
        "cupon": cupon_descuento
    })

    response_id_4 = requests.post(url, headers=headers, data=payload_id_4)
    response_data_id_4 = None

    if response_id_4.status_code == 200:
        response_data_id_4 = response_id_4.json()
    print("Valor de response_data_id_4:", response_data_id_4)
    print("Respuesta de la API:", response_data_id_3,response_data_id_4)
    print("Datos enviados en la solicitud:", payload_id_3,payload_id_4)
    print("a",response_id_4)

    
    precio3 = float(response_data_id_3.get("precio", "0")) if response_data_id_3 else 0
    precio4 = float(response_data_id_4.get("precio", "0")) if response_data_id_4 else 0


    porcentaje_impuesto = response_data_id_3.get("porcentaje_impuesto", "No disponible")if response_data_id_3 else "No disponible"
            

    total_pagar3 = response_data_id_3.get("total_pagar", "No disponible")if response_data_id_3 else "No disponible"
    total_pagar4 = response_data_id_4.get("total_pagar", "No disponible")if response_data_id_4 else "No disponible"
    print("Precio:", precio3,precio4)
    print("Porcentaje de Impuesto:", porcentaje_impuesto)
    print("Total a Pagar:", total_pagar3,total_pagar4)     

    try:
        
        propuesta = nueva_propuesta.objects.get(id=propuesta_id)


        
        informe_data = generar_informe(propuesta)

        return render(request, 'oferta/informe.html', {
            'informe_data': informe_data,
            'precio3': precio3,
            'precio4': precio4,
            'porcentaje_impuesto': porcentaje_impuesto,
            'total_pagar3': total_pagar3,
            'total_pagar4': total_pagar4,
            'descuento': precio3 * 2 - precio4,
        })
        
    except nueva_propuesta.DoesNotExist:
        return render(request, 'oferta/informe.html', {'informe_data': None})

def mostrar_alerta(request):
    mensaje = 'Ya existe una propuesta con el mismo número de documento o nombre/razón social.'
    return render(request, 'alerta.html', {'mensaje': mensaje})

def enviar_correo(asunto, mensaje, destinatarios, remitente):
    try:
        send_mail(asunto, mensaje, remitente, destinatarios)
        print(f"Correo enviado a {', '.join(destinatarios)}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def eliminar_propuesta( request, id):
    try:
        propuesta = nueva_propuesta.objects.get(id=id)
    except nueva_propuesta.DoesNotExist:
        raise Http404("La propuesta no existe")  

    propuesta.delete()
    return redirect('oferta')


"""
def descargar_pdf(request):
    # Ruta de la plantilla HTML que deseas convertir a PDF

    vista = 'oferta/informe.html'
    
    template = get_template(vista)
    html = template.render()
    
    
    result = BytesIO()
    html2 = BytesIO(html.encode('utf-8'))

    response = HttpResponse(html, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename=informe.html'
    return response 
     pdf = pisa.CreatePDF(html2, result)
    
    if not pdf.err:
        # Si la generación del PDF fue exitosa, regresa el PDF como una descarga.
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=propuesta.pdf'
        return response

    return HttpResponse('Hubo un error al generar el PDF', status=400)
    """