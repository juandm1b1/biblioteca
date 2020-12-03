import json # Para crear JSON, viene del lenguaje, no del framework. Importación para 1ra forma de obtener JSON para petición AJAX
#from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.serializers import serialize # Importación para 2da forma de obtener JSON para petición AJAX
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from apps.usuario.models import Usuario
from apps.usuario.forms import FormularioLogin, FormularioUsuario


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)

    
    def form_valid(self, form):
        login(self.request, form.get_user()) # Que con datos que se pasan en el formluario se inicie una sesión
        return super(Login, self).form_valid(form)


def logoutUsuario(request):
    logout(request)    
    return HttpResponseRedirect('/accounts/login/')



class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('usuarios:listado_usuarios')

    # def post(self,request,*args,**kwargs): # Para usar diccionario cleaned_data se sobreescribe post()
    #     form = self.form_class(request.POST)
    #     #print(form.cleaned_data)
        
    #     """ No se usa para la creación de un nuevo usuario 'Usuario.objects.create()' porque una vez se crea la instancia se debe
    #     encriptar la contraseña antes de guardar en la BD 
    #     """
    #     if form.is_valid(): # Incluye la validación agregada de clean_password2()
    #         nuevo_usuario = Usuario(
    #             email = form.cleaned_data.get('email'),
    #             username = form.cleaned_data.get('username'),
    #             nombres = form.cleaned_data.get('nombres'),
    #             apellidos = form.cleaned_data.get('apellidos')
    #         )
    #         nuevo_usuario.set_password(form.cleaned_data.get('password1'))
    #         nuevo_usuario.save() # Save del modelo, si por algún motivo se llama 1ro el save() del formulario y luego el del modelo, se encripta 2 veces la contraseña
    #         return redirect('usuarios:listado_usuarios')
    #     else:
    #         return render(request, self.template_name,{'form':form})

""" Se separa la vista Listar usuario en 2: una que renderice el template y otra que tenga la consulta para solucionar bug de que se muestra json al dar 'atrás' en el navegador
La idea es redireccionar a 'InicioListarUsuario' cada vez que se intente acceder por una petición NO AJAX al listado de usuarios.

Al ser una vista sin codigo añadido o métodos sobreescritos, se puede 'crear'/'usar' directamente en urls.py

class InicioListarUsuario(TemplateView): 
    template_name = 'usuarios/listar_usuario.html'

"""


class ListarUsuario(ListView):
    model = Usuario
    #template_name = 'usuarios/listar_usuario.html' # Esto se pasa a 'InicioListarUsuario'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)


    """ 2. Segunda forma de obtener JSON para la petición AJAX:
    
        Se sobreescribe el método GET para que el listado de Usuarios se realice por medio de petición AJAX 
        Se 

        SE DEBE VALIDAR NO SOLO QUE LA PETICIÓN SEA DE TIPO GET, SINO TAMBIÉN AJAX:
        Hay 2 peticiones: Una es la AJAX que la hace JS con la función jQuery en index.js, la otra es la http normal del navegador.
        Por eso se utiliza el if en la función GET, para saber el return a hacer

    """
    def get(self,request,*args,**kwargs):
        if request.is_ajax(): # is_ajax(): Función integrada en Django            
            
            data = serialize('json', self.get_queryset()) # Para convertir a JSON la lista de usuarios; solo hay que usar el método serialize indicando el tipo de archivo y la consulta
            print(self.kwargs) # Por ser diccionario los parámetros exta en el path de urls.py, viene en los Kwargs
            return HttpResponse(data,'application/json') # Se retorna como HttpResponse e indicar que es 'application/json'

        else:
            return redirect('usuarios:inicio_usuarios') 
            #return render(request,self.template_name) # En vez de renderizar se realiza redireccionamiento a url de view 'InicioListarUsuario'


    """ 1. Primera forma de obtener JSON para la petición AJAX:
    
        Se sobreescribe el método GET para que el listado de Usuarios se realice por medio de petición AJAX 
        Se crea un diccionario 'data_usuario' en el que se se guardan c/u de las propiedades de las instancias del modelo Usuario obtenidas en la consulta.
        Luego se guardan c/u de los diccionarios creados en la lista de usuarios

        SE DEBE VALIDAR NO SOLO QUE LA PETICIÓN SEA DE TIPO GET, SINO TAMBIÉN AJAX:
        Hay 2 peticiones: Una es la AJAX que la hace JS con la función jQuery en index.js, la otra es la http normal del navegador.
        Por eso se utiliza el if en la función GET, para saber el return a hacer

    
    def get(self,request,*args,**kwargs):
        if request.is_ajax(): # is_ajax(): Función integrada en Django

            lista_usuarios = [] # Para colocar c/u de los registros obtenidos de la consulta
            for usuario in self.get_queryset():
                data_usuario = {}
                data_usuario['id'] = usuario.id
                data_usuario['username'] = usuario.username
                data_usuario['nombres'] = usuario.nombres
                data_usuario['apellidos'] = usuario.apellidos
                data_usuario['email'] = usuario.email
                data_usuario['usuario_activo'] = usuario.usuario_activo
                lista_usuarios.append(data_usuario)
            
            data = json.dumps(lista_usuarios) # Para convertir a JSON la lista de usuarios; realmente crea un str de la lista

            return HttpResponse(data,'application/json') # Se retorna como HttpResponse e indicar que es 'application/json'

        else:
            return render(request,self.template_name)

    """

    

