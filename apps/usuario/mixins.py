from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class LoginYUsuarioStaffMixin(object):
    """ Clase Mixin personalizada para validar 1: Si está autenticado, 2: Si es staff """    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return super().dispatch(request, *args, **kwargs)
        return redirect('index')


class LoginMixin(object):
    """ Clase Mixin personalizada para validar 1: Si está autenticado """    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')


class ValidarPermisosMixin(object):
    """ Clase Mixin personalizada para validar si usuario cuenta con permisos 
        Sustituye a 'PermissionRequiredMixin', que por defecto lanza error 403 Forbbiden cuando se accede a una ruta para la cual no se tiene permiso.
        SI SE DESEA GENERALIZAR 'ValidarPermisosRequeridosMixin' no solo para usuarios, 'permission_required' SE DEBE DEFINIR EN CADA VISTA,
        y quedar aquí en el Mixin ** permission_required = '' **
    """
    permission_required = ('usuario.view_usuario','usuario.add_usuario','usuario.change_usuario','usuario.delete_usuario')
    url_redirect = None
    
    def get_perms(self):
        """ Método para obtener los permisos. Si hay permisos de la instancia convertida a cadena, hace una tupla con estos,
            si no retornarlo porque ya es tupla
        """
        if isinstance(self.permission_required,str):
            perms = (self.permission_required)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        """ Método que manda al la url login si el self no tiene url para redirigir
        """
        if self.url_redirect is None:
            return reverse_lazy('login')        
        return self.url_redirect

    
    def dispatch(self, request, *args, **kwargs):
        """ Si tiene permisos, que continúe con la ejecución, sino que redireccione a lo que retorna get_url_redirect() 
        """
        if request.user.has_perms(self.get_perms()): # Se declaró metodo 'get_perms()' para poder pasar el parámetro a has_perms(perm_list)
            return super().dispatch(request, *args, **kwargs)
        messages.error(request,'No tienes permisos para realizar esta acción.') # Se define mensaje de error      
        return redirect(self.get_url_redirect())

    

    
    

# """ Validar si un Usuario es Superusuario. Hereda de Object, que es la raíz de donde heredan todas las clases de Python """
# class SuperusuarioMixin(object):
#     """ Se sobrescribe dispatch. Todas las vistas basadas en clase tienen este método, 
#     que verifica qué método HTTP se ha utilizado para poder redireccionar y llamar al método correspondiente.
#     Este Mixin es para ser aplicado a la Vista 'ListarUsuario' que es la principal
#     """
#     def dispatch(self, request, *args, **kwargs): 
#         """ Si es Staff/Administrador/Superusuario, que continúe normal con la ejecución de los métodos,
#         si no, que lo redireccione al index.
#          """       
#         if request.user.is_staff: # 'is_staff', método que se definió en models.py, que retorna si el Usuario es Admin/Superusuario o no
#             return super().dispatch(request, *args, **kwargs)
#         return redirect('index')
        
    