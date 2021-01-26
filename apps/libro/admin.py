from django.contrib import admin
from django.db.models import Q

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Autor, Libro, Reserva
from .forms import ReservaForm # Para modificar form en el admin, de forma que no aparezcan en la lista de reserva libros con cantidad 0


class ReservaAdmin(admin.ModelAdmin):
    form = ReservaForm
    list_display = ('libro','usuario','estado','fecha_creacion')


class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo','obtener_autores','cantidad','estado','fecha_creacion')


# Clase para botones importar-exportar en el admin. Es como una 'plantilla', parecido a ModelForm
class AutorResource(resources.ModelResource):
    class Meta:
        model = Autor
        list_display = ('libro','usuario','estado','fecha_creacion')


class AutorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('nombre', 'apellido', 'pais', 'estado')
    list_display = ('nombre', 'apellido', 'pais', 'estado')
    resource_class = AutorResource
    actions = ['eliminacion_logica_autores', 'activacion_logica_autores'] #Acciones que se quiere que aparezcan en en admin. Si la función está dentro de la clase, se pone su nombre entre comillas. Si está por fuera, no.

    def eliminacion_logica_autores(self, request, queryset):        
        for autor in queryset:
            autor.estado = False
            autor.save()

    def activacion_logica_autores(self, request, queryset):        
        for autor in queryset:
            autor.estado = True
            autor.save()            
    
    # def eliminacion_autores_con_filtro(self, request, queryset): # Se cambia modeladmin por self al pasar la función adentro de la clase
    #     queryset = queryset.exclude(Q(nombre__icontains = 'Mau') | Q(nombre__icontains = 'And') | Q(nombre__icontains = 'Mau') | Q(nombre__icontains = 'Mau'))

    #     for autor in queryset:
    #         autor.delete()


    # # Sobreescritura de función get_actions para quitar opción de eliminar seleccionados en el admin y que solo se pueda hacer desde la BD
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
        
    #     return actions


admin.site.register(Autor, AutorAdmin) 
admin.site.register(Libro, LibroAdmin)
admin.site.register(Reserva, ReservaAdmin)




# class LibroAdmin(admin.ModelAdmin):
#     #lib = Libro()
#     # autores = []
#     # for autor_id in lib:
#     #     autores.add[autor_id]


#     list_display = ('titulo', 'autor_id')