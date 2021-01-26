"""biblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
#from django.contrib.auth import logout
#from django.contrib.auth.views import login, logout_then_login -YA NO EXISTE-  # Para iniciar y cerrar sesión. SON FUNCIONES. No necesitan Views(son Views), solo template y url
from django.contrib.auth.decorators import login_required
#from apps.libro.views import Inicio
from apps.usuario.views import Inicio, Login, logoutUsuario


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/',include(('apps.usuario.urls', 'usuarios'))),
    path('', Inicio.as_view(), name='index'),    
    path('libro/', include(('apps.libro.urls', 'libro'))),
    path('accounts/login/', Login.as_view(), name = 'login'),
    path('logout/', login_required(logoutUsuario), name = 'logout'),
    # ---YA NO EXISTEN-------
    # path('accounts/login/', login, {'template_name': 'login.html'}, name = 'login'), # Se llama la función login, para indicarle el template path y re_path permiten enviar argumentos como diccionario
    # path('logout/', logout_then_login, name = 'logout'),
]

# Se agrega url para serir archivos Media
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]