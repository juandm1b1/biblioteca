from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.core.serializers import serialize # Importación para 2da forma de obtener JSON para petición AJAX
from django.http import HttpResponse, JsonResponse
from .forms import AutorForm, LibroForm
from .models import Autor, Libro
#from .serializers import AutorSerializer, LibroSerializer NO SE USÓ


"""
Constructor Módulo 'View': ('View' es la clase base de la cual heredan las demás, y  se utiliza cuando va a haber lógica; 
si sólo se va a renderizar un template se utiliza 'TemplateView').

Métodos integrados en la clase View (y que heredan TemplateView, ListView, CreateView, UpdateView):
1. método dispatch(): valida la petición y elige que método HTTP se utilizó para la solicitud
2. http_method_not_allowed(): retorna error cuando se utiliza un método HTTP no soportado o definido. 
Verifica que método devolvió dispatch y si tiene implementación. De no ser así invoca el http not allowed
3. options(): responden a las peticiones options de HTTP, por lo general no se sobreescribe

"""

class Inicio(TemplateView):
    template_name = 'index.html' 


 # ListView -> 'Consultar': SELECT * FROM interno. RETORNA UNA LISTA DE OBJETOS, por lo que en el Template se debe llamar como 'object_list'
class ListadoAutor(View): # Se cambia ListView por View para usar el Método post e INCLUIR EL FORM DE REGISTRO EN EL LISTADO DE AUTORES
    model = Autor
    form_class = AutorForm
    #template_name = 'libro/autor/listar_autor.html'    
    #context_object_name = 'autores' #Si se quiere personalizar el nombre de 'object_list'

    def get_queryset(self):
        return self.model.objects.filter(estado=True)
    
    def get_context_data(self,**kwargs):
        ctx = {}
        ctx['autores'] = self.get_queryset()
        ctx['form'] = self.form_class
        return ctx

    def get(self,request,*args,**kwargs):
        if request.is_ajax():
            data = serialize('json', self.get_queryset())
            return HttpResponse(data,'application/json')
        else:
            return redirect('libro:inicio_autores')
        #return render(request,self.template_name,self.get_context_data())

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libro:listar_autor')  


class CrearAutor(CreateView): # INSERT
    model = Autor
    form_class = AutorForm    
    template_name = 'libro/autor/crear_autor.html'    
    success_url = reverse_lazy('libro:inicio_autores')

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje,'error':error}) 
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            redirect('libro:inicio_autores')
        


class EditarAutor(UpdateView): # UPDATE
    model = Autor
    form_class = AutorForm    
    template_name = 'libro/autor/editar_autor.html'    
    #success_url = reverse_lazy('libro:listar_autor')  

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(*kwargs)
    #     ctx['autores'] = self.model.objects.filter(estado=True)
    #     return ctx

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} se ha actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            redirect('usuarios:inicio_usuarios')


    """ 
    En vistas basadas en clases, el parámetro en la url debe ser 'pk' o 'slug', y el form debe ser llamado en el template como 'form'
    """

class EliminarAutor(DeleteView):
    model = Autor    
    success_url = reverse_lazy('libro:listar_autor') # Este se quita porque es para el borrado total   

    def delete(self,request,*args,**kwargs):
        if request.is_ajax():
            autor = self.get_object()
            autor.estado = False
            autor.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje':mensaje,'error':error})
            response.status_code = 201
            return response
    
    #     # Se sobreescribe el método post para hacer que el borrado sea lógico y no definitivo de la BD
    # def post(self,request,pk,*args,**kwargs):
    #     autor = Autor.objects.get(id=pk)
    #     autor.estado = False
    #     autor.save() 
    #     return redirect('libro:listar_autor')

    """
    En DeleteView se debe crear una template "nombreModelo_confirm_delete.html" que es la de confirmación de eliminación    
    En los template con vistas basadas en clase las instancias de los objetos (ctx) se llaman como 'object'    """


class ListadoLibros(View): # Se cambia ListView por View para usar el Método post e INCLUIR EL FORM DE REGISTRO EN EL LISTADO DE LIBROS
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/listar_libro.html'    

    # RETORNA LA CONSULTA
    def get_queryset(self):  # Este método se ejecuta automáticamente en ListView al crear 'queryset'. Se sobreescribe para ser usado a nivel de clase y no solo en el método              
        return Libro.objects.filter(estado=True)

    # RETORNA EL CONTEXTO A ENVIAR AL TEMPLATE
    def get_context_data(self,**kwargs): # Método automático en ListView ('context_object_name'). Para retornar Contexto a nivel de clase
        ctx = {}
        ctx['libros'] = self.get_queryset()
        ctx['form'] = self.form_class
        return ctx
    
    # RETORNA EL RENDERIZADO CON LA PETICIÖN HTTP MËTODO GET    
    def get(self,request,*args,**kwargs):
        if request.is_ajax():
            qs = self.get_queryset()            
            data = serialize('json', qs, use_natural_foreign_keys=True) # 'use_natural_foreign_keys' permite ver otros atributos de ForeignKeys o ManyToManyFields diderentes al id          
            return HttpResponse(data,'application/json')
        else:
            return redirect('libro:inicio_libros')             
        # ctx = {'libros': self.get_queryset()} # En vez de esta consulta, se trae el contexto desde get_context_data
        #return render(request, self.template_name, self.get_context_data())

    # RETORNA EL RENDERIZADO CON LA PETICIÖN HTTP MËTODO POST
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('libro:listar_libros')


class CrearLibro(CreateView): 
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    #success_url = reverse_lazy('libro:listar_libros')    

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():                
                form.save()
                mensaje = f'{self.model.__name__} creado correctamente!'
                error = "Sin errores!"
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido crear!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            redirect('libro:listar_libros')



class EditarLibro(UpdateView):
    model = Libro
    form_class =LibroForm
    template_name = 'libro/libro/editar_libro.html' # Este template es donde está definido el Modal de edición de libro
    #success_url = reverse_lazy('libro:listar_libros')

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs) # Si se quita el parámetro **kwargs, igual funciona
        ctx['libros'] = Libro.objects.filter(estado=True)
        return ctx     

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} editado con éxito!'
                error = 'Sin errores!'
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no ha podido ser editado!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            redirect('libro:inicio_libros')



class EliminarLibro(DeleteView):
    model = Libro    
    success_url = reverse_lazy('libro:listar_libros')
    #queryset = self.model.objects.get(id=pk)

    def delete(self,request,*args,**kwargs):
        if request.is_ajax():
            libro = self.get_object()
            libro.estado = False
            libro.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje':mensaje,'error':error})
            response.status_code = 201
            return response

    # def post(self,request,pk,*args,**kwargs):
    #     if request.is_ajax():
    #         libro = queryset
    #         # libro = Libro.objects.get(id=pk)
    #         libro.estado = False
    #         libro.save()
    #         return redirect('libro:listar_libros')













# -------------CON FUNCIONES y opciones no ideales con Views-------------------------------------------------

# class Inicio(View): # 'TemplateView' solo tiene definido el método get
#     def get(self, request, *args, **kwargs):
#         return render(request,'index.html')


# def home(request):
#     return render(request, "index.html")
# --------------------------------------------------------------------------------------------
# class ListadoAutor(TemplateView): # Se puede traer consulta con TemplateView sobreescribiendo el método get
#     template_name = 'libro/listar_autor.html'

#     def get(self, request, *args, **kwargs):
#         autores = Autor.objects.filter(estado=True)
#         return render(request, self.template_name, {'autores':autores})   


# def listarAutor(ListView):
#     autores = Autor.objects.filter(estado = True) # Por borrado lógico
#     return render(request, "libro/listar_autor.html", {'autores': autores})

#----------------------------------------------------------------------------------------------

# def crearAutor(request):
#     if request.method == 'POST':
#         autor_form = AutorForm(request.POST)
#         if autor_form.is_valid():
#             autor_form.save()
#             return redirect('libro:listar_autor')
#     else:
#         autor_form = AutorForm()

#     return render(request, "libro/crear_autor.html", {'autor_form': autor_form})

#----------------------------------------------------------------------------------------------

# def editarAutor(request, id):
#     autor_form = None
#     error = None

#     try:
#         autor = Autor.objects.get(id = id)
        
#         if request.method == 'GET':
#             autor_form = AutorForm(instance = autor)
#         else:
#             autor_form = AutorForm(request.POST, instance = autor)
            
#             if autor_form.is_valid():
#                 autor_form.save()
#             return redirect('libro:listar_autor')

#     except ObjectDoesNotExist as e:  
#         error = e   

#     return render(request, "libro/crear_autor.html", {'autor_form': autor_form, 'error': error})

#-------------------------------------------------------------------------------------------------


# def eliminarAutor(request, id):   
   
#     autor = Autor.objects.get(id = id)

#     if request.method == 'POST':        
#         autor.estado = False # Eliminación lógica
#         autor.save()
#         return redirect('libro:listar_autor')
    
#     return render(request, "libro/eliminar_autor.html", {'autor': autor})

