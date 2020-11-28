from django.contrib import admin

from .models import Autor, Libro


# class LibroAdmin(admin.ModelAdmin):
#     #lib = Libro()
#     # autores = []
#     # for autor_id in lib:
#     #     autores.add[autor_id]


#     list_display = ('titulo', 'autor_id')


admin.site.register(Autor) 
admin.site.register(Libro)