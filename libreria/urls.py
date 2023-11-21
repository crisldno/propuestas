from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import Logueo
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', Logueo.as_view(), name='logueo'),
    path('login/', Logueo.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='logueo'), name='logout'),
    path('oferta/', views.oferta, name='oferta'),
    path('descargar_propuestas/', views.descargar_excel, name='descargar_propuestas'),
    path('oferta/crear/', views.crear, name='crear'),
    path('oferta/editar/', views.editar, name='editar'),
    path('crear_propuesta/', views.crear_propuesta, name='crear_propuesta'),
    path('confirmacion/',views.confirmacion, name='confirmacion'),
    path('informe/', views.informe, name='informe'),
    #path('crear_propuesta/alerta/', views.mostrar_alerta, name='alerta'),
    path('informe/<int:propuesta_id>/', views.informe, name='informe'),
    path('eliminar_propuesta/<int:id>/', views.eliminar_propuesta, name='eliminar_propuesta'),
    #path('descargar_pdf/', views.descargar_pdf, name='descargar_pdf'),
    path('enviar_propuesta/', views.enviar_propuesta, name='enviar_propuesta'),
    
    
]  