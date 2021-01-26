from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  # User 
""" Si se quiere agregar campos al modelo user por defecto, se importa User y se agrega en el modelo creado como Foreign Key 
'AbstractBaseUser' es la clase de la cual hereda User, y se usa para 'personalizar' el modelo Usuario y no usar el por defecto

""" 

""" BaseUserManager: Es la base para crear un Manager relacionado a un modelo Usuario. Es necesario por como funciona el ORM de Django.
En esta clase se definen 2 funciones, una para crear un usuario básico, y otra para crear un usuario administrador
"""
class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, nombres, password, is_staff, is_superuser, **extra_fields): #Función para crear usuarios a ser llamada cuando se use la consola
        user = self.model(
            username=username, 
            email=self.normalize_email(email), 
            nombres=nombres,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password=password
        user.save(self.db)
        return user

    def create_user(self, username, email, nombres, password = None, **extra_fields): #Función para crear usuarios normales, no son ni staff ni superuser
        return self._create_user(username, email, nombres, password, False, False, **extra_fields)

    def create_superuser(self, username, email, nombres, password = None, **extra_fields): #Función para crear superusuarios
        return self._create_user(username, email, nombres, password, True, True, **extra_fields)


""" Para utilizar permisos usuarios personalizados hay que usar la clase PermissionMixin:
    Para definir un Permissionixin propio, hay que crear nuestra propia clase PermissionMixin y agregársela como Herencia a la Clase Usuario.
    Además hay que corregir el Modelo Usuario así como su Manager para poder utilizar los Permisos.
    1. Se cambian campos 'usuario_activo' y 'usuario_administrador' por 'is_active' y 'is_staff' respectivamente.
    2. Se quitan todos los métodos sobreescritos ya que lo va a manejar internamente 'PermissionsMixin'
    3. Se redefine todo el 'UsuarioManager'
 """


class Usuario(AbstractBaseUser,PermissionsMixin): #(User). 
    
    """'PermissionsMixin': Para manejar permisos de Usuarios. Al hacer nuevamente las migraciones despues de agregarlo, 
    se incluyen los siguientes campos en el modelo Usuario:
    - Add field groups to usuario
    - Add field is_superuser to usuario
    - Add field user_permissions to usuario
    """
    # usuario = models.ForeignKey(User, on_delete=CASCADE)
    username = models.CharField(verbose_name='Nombre de Usuario', unique=True, max_length=100)
    email = models.EmailField(verbose_name='Correo Electrónico', unique=True, max_length=254)
    nombres = models.CharField(verbose_name='Nombres',max_length=200,blank=True, null=True)
    apellidos = models.CharField(verbose_name='Apellidos',max_length=200,blank=True, null=True)
    imagen = models.ImageField(verbose_name='Imagen de Perfil', upload_to='perfil/', max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # 'is_staff' define si piede acceder al sitio de Administración de Django
    
    objects = UsuarioManager() # Campo que enlaza las 2 funciones de creación de usuario en UsuarioManager

    """ AbstractBaseUser tiene: USERNAME_FIELD, que es parámetro que va a diferenciar al usuario y siempre va a ser requerido.
    Siempre es el username o el email.
    REQUIRED_FIELDS: Lista de campos obligatorios
    """
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos']

    """ La definición de clase Meta permite traer atributo 'permissions' para crear permisos personalizados:
        Extra permissions to enter into the permissions table when creating this object. 
        Add, change, delete, and view permissions are automatically created for each model. 
        permissions = [('permission_code', 'human_readable_permission_name')]
     """
    class Meta:
        permissions = [('permiso_desde_codigo','Permiso creado desde el código'),] # Pueden ser varios permisos (Tuplas). Se deben hacer migraciones


    def __str__(self):
        return f'Usuario {self.username}' #Sintaxis 'F string'


    """ Se quitan todos los métodos sobreescritos ya que lo va a manejar internamente 'PermissionsMixin' """

    # """ método has_perm(): 'AbstractBaseUser' necesita diversas utilidades para que se pueda utilizar el modelo 
    # usuario en el admin de Django. Este método es llamado por el admin de Django en la parte de los permisos de quein puede acceder o no al Admin
    # Si se quiere que aparezca en el admin se debe definir
    # """
    # def has_perm(self,perm,obj = None):
    #     return True

    # """ Método has_module_perms(): También para el admin de Django. Recibe la etiqueta de la app en la cual está este modelo 
    # """
    # def has_module_perms(self,app_label):
    #     return True

    # """ Definición de propiedades. is_staff() viene también definido en User de Django y valida si un usuario es Admin o no
    # """
    # @property
    # def is_staff(self):
    #     return self.usuario_administrador   


    # ----------- UsuarioManager Antiguo -------------------------
    """
    class UsuarioManager(BaseUserManager):

    def create_user(self,email,username,nombres,apellidos,password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username=username, 
            email=self.normalize_email(email), 
            nombres=nombres, 
            apellidos=apellidos
        ) # normalize_email: función incorporada en BaseUserManager para normalizar y poder validar email

        usuario.set_password(password) # Uso de encriptación incorporada en BaseUserManager para la contraseña, con el método set_password()
        usuario.save()        
        return usuario

    def create_superuser(self,email,username,nombres,apellidos,password):
        usuario = self.create_user(
            email,
            username=username,            
            nombres=nombres, 
            apellidos=apellidos,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario
    """