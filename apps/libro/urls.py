from django.urls import path, re_path
from django.contrib.auth.decorators import login_required  # Para garantizar logueo antes de mostrar la URL
from django.views.generic import TemplateView # Para la vista que solo renderiza template
from . import views


urlpatterns = [    
    path('crear_autor/', login_required(views.CrearAutor.as_view()), name='crear_autor'),
    path('listar_autor/', login_required(views.ListadoAutor.as_view()), name='listar_autor'),
    path('editar_autor/<int:pk>/', login_required(views.EditarAutor.as_view()), name ='editar_autor'),
    path('eliminar_autor/<int:pk>/', login_required(views.EliminarAutor.as_view()), name ='eliminar_autor'),
    #re_path(r'^editar_autor/(?P<id>\)', views.EditarAutor, name ='editar_autor'),
    #re_path(r'^eliminar_autor/(?P<id>\)', views.EliminarAutor, name ='eliminar_autor'),

    path('listar_libros/', login_required(views.ListadoLibros.as_view()), name = 'listar_libros'),
    path('crear_libro/', login_required(views.CrearLibro.as_view()), name = 'crear_libro'),
    path('editar_libro/<int:pk>/', login_required(views.EditarLibro.as_view()), name = 'editar_libro'),
    path('eliminar_libro/<int:pk>/', login_required(views.EliminarLibro.as_view()), name = 'eliminar_libro'),
] 

# URLS de vistas "implícitas"
urlpatterns += [
    path('inicio_autores/', login_required(TemplateView.as_view(template_name = 'libro/autor/listar_autor.html')), name = 'inicio_autores'),
    path('inicio_libros/', login_required(TemplateView.as_view(template_name = 'libro/libro/listar_libro.html')), name = 'inicio_libros'),
    # Se pasa como parámetro al método as_view() el template_name (y los demás necesarios)
]