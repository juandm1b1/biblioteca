from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import AutorForm, LibroForm
from .models import Autor, Libro


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


class ListadoAutor(ListView): # 'Consultar': SELECT * FROM interno. RETORNA UNA LISTA DE OBJETOS, por lo que en el Template se debe llamar como 'object_list'
    model = Autor
    template_name = 'libro/autor/listar_autor.html'
    #context_object_name = 'autores' #Si se quiere personalizar el nombre de 'object_list'
    queryset = Autor.objects.filter(estado=True)


class CrearAutor(CreateView): # INSERT
    model = Autor    
    template_name = 'libro/autor/crear_autor.html'
    form_class = AutorForm
    success_url = reverse_lazy('libro:listar_autor')


class EditarAutor(UpdateView): # UPDATE
    model = Autor    
    template_name = 'libro/autor/crear_autor.html'
    form_class = AutorForm
    success_url = reverse_lazy('libro:listar_autor')    

    """ 
    En vistas basadas en clases, el parámetro en la url debe ser 'pk' o 'slug', y el form debe ser llamado en el template como 'form'
    """

class EliminarAutor(DeleteView):
    model = Autor    
    #success_url = reverse_lazy('libro:listar_autor') # Este se quita porque es para el borrado total   
    
    # Se sobreescribe el método post para hacer que el borrado sea lógico y no definitivo de la BD
    def post(self,request,pk,*args,**kwargs):
        autor = Autor.objects.get(id=pk)
        autor.estado = False
        autor.save() 
        return redirect('libro:listar_autor')

    """
    En DeleteView se debe crear una template "nombreModelo_confirm_delete.html" que es la de confirmación de eliminación    
    En los template con vistas basadas en clase las instancias de los objetos (ctx) se llaman como 'object'
    """


class ListadoLibros(ListView):
    model = Libro
    template_name = 'libro/libro/listar_libro.html'
    queryset = Libro.objects.filter(estado=True)


class CrearLibro(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    success_url = reverse_lazy('libro:listar_libros')


class EditarLibro(UpdateView):
    model = Libro
    form_class =LibroForm
    template_name = 'libro/libro/crear_libro.html'
    success_url = reverse_lazy('libro:listar_libros')


class EliminarLibro(DeleteView):
    model = Libro    
    #success_url = reverse_lazy('libro:listar_libros')

    def post(self,request,pk,*args,**kwargs):
        libro = Libro.objects.get(id=pk)
        libro.estado = False
        libro.save()
        return redirect('libro:listar_libros')




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

