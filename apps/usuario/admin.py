from django.contrib import admin
from django.contrib.auth.models import Permission # Para agregar permisos a admin
from django.contrib.contenttypes.models import ContentType
from apps.usuario.models import Usuario

admin.site.register(Usuario)
admin.site.register(Permission)
admin.site.register(ContentType)
""" Django crea 4 Permisos por cada Modelo al realizar la migración, y los añade a un Modelo que se llama 'Permission' 
    Se pueden verificar en el Admin
"""
