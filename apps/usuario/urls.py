from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView # Para la vista que solo renderiza template
from apps.usuario import views

urlpatterns = [   
    path('inicio_usuarios/', views.InicioUsuarios.as_view(), name = 'inicio_usuarios'),
    # Se pueden pasar parámetros extra en el path, en 3er lugar después de la vista, como diccionario, y ser usado en la view llamando el parámetro
    path('listado_usuarios/', views.ListarUsuario.as_view(), {'parametro_extra': 'Hola gonohp carech'}, name = 'listado_usuarios'),
    path('registrar_usuario/', views.RegistrarUsuario.as_view(), name = 'registrar_usuario'),
    path('editar_usuario/<int:pk>/', views.EditarUsuario.as_view(), name = 'editar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.EliminarUsuario.as_view(), name = 'eliminar_usuario'),   
]   

# URLS de vistas "implícitas"
# urlpatterns += [
#     path('inicio_usuarios/', login_required(TemplateView.as_view(template_name = 'usuarios/listar_usuario.html')), name = 'inicio_usuarios'),
#     # Se pasa como parámetro al método as_view() el template_name (y los demás necesarios)
    # Vuelve a views.py para aoplicarle mixin
# ]