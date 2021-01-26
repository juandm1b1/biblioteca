from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save, post_delete # Para el Signal

from apps.usuario.models import Usuario

""" Después del elimiado lógico de un autor, este sigue apareciendo al listar o registrar un libro. Para poder eliminar este error se necesitan los
    SIGNALS, porque si se hiciera directamente en la vista funcionaria desde la app pero no desde el admin. Antes de usar signal hay que saber que cuando se usa el método 'save()' se ejecutan automática/. varias funciones, una de las cuales 
    valida los campos del modelo:  Clean(), FuulClean(), CleanFields(), etc.
    Clean(): Se ejecuta antes de proceder a crear, guardar, eliminar, editar la instancia del modelo. Sirve para validar los cambios antes de
    efectuar el save() """

""" SIGNALS: Son como los TRIGGERS en las BD. COnjunto de código que se ejecuta cuando se efectúan acciones CRUD.
    'post_save()': va a permitir quitar la relación de todo Autor eliminado con los Libros
    SE BUSCA QUE SE EJECUTE UN SIGNAL DESPÚES DE QUE SE GRABE UNA INSTANCIA DE AUTOR """

# Manager permite en este caso utilizar 'natural keys' (en este caso nombres y apellidos) en vez de la pk para el ManyToManyField 'autor_id' en el modelo Libro
class AutorManager(models.Manager):
    def get_by_natural_key(self, apellido, nombre):
        return self.get(apellido=apellido, nombre=nombre)   

class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=False, null=False, verbose_name='Nombres')
    apellido = models.CharField(max_length=220, blank=False, null=False, verbose_name='Apellidos')
    pais = models.CharField(max_length=100, blank=False, null=False, verbose_name='País')
    descripcion = models.TextField(blank=False, null=False, verbose_name='Descripción')
    estado = models.BooleanField('Estado', default=True) # Para borrado lógico y no definitivo de la BD
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now=True, auto_now_add=False)

    objects = AutorManager()
    
    class Meta:
        unique_together = [['apellido', 'nombre']]
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['apellido']

    # Método que retorna la 'natural key' en las relaciones con otras tablas, en vez de la pk
    def natural_key(self):
        return (self.apellido + ', ' + self.nombre)

    def __str__(self):
        return self.apellido + ", " + self.nombre


class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField('Título', max_length=255, blank=False, null=False) 
    descripcion = models.TextField('Descripción', null=True, blank=True)
    cantidad = models.SmallIntegerField('Cantidad o Stock', default = 1)
    imagen = models.ImageField('Imagen', upload_to='libros/', max_length=255, null= True, blank= True)
    autor_id = models.ManyToManyField(Autor, verbose_name='Autor(es)')
    fecha_publicacion = models.DateField('Fecha de publicación', blank=False, null=False)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now=True, auto_now_add=False)
    

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def natural_key(self):
        return self.titulo

    def __str__(self):
        return self.titulo

    # Método para obtener autores del libro y usarlo en la template 'detalle_libro_disponible.html -> object.obtener_autores'
    def obtener_autores(self):
        autores = str([autor for autor in self.autor_id.all().values_list('nombre', flat=True)]).replace("[","").replace("]","").replace("'","")
        return autores


class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad_dias = models.SmallIntegerField('Cantidad de días a reservar', default = 7)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):    
        return f'Reserva de libro {self.libro} por {self.usuario}'


# Código para la Signal:
""" Sender: El modelo del que viene la señal
    instance: Instancia del modelo sender
    post_save.connect: Método para conectar el método con el sender
"""
def quitar_relacion_autor_libro(sender,instance,**kwargs):
    if instance.estado == False:
        autor = instance.id
        libros = Libro.objects.filter(autor_id=autor)
        for libro in libros:
            libro.autor_id.remove(autor)


def reducir_cantidad_libro(sender,instance,**kwargs):
    libro = instance.libro # Se saca el campo 'libro de la instancia, 'reserva'
    if libro.cantidad > 0:
        libro.cantidad = libro.cantidad - 1        
        if libro.cantidad <= 0:
            libro.estado = False
    libro.save()

def aumentar_cantidad_libro_delete(sender, instance, **kwargs):
    libro = instance.libro
    libro.cantidad += 1
    libro.estado = True
    libro.save()

# def aumentar_cantidad_libro_update(sender, instance, **kwargs):
#     #libro = instance.libro
#     if instance.cantidad >= 1:
#         instance.estado = True
#         instance.save()


# # Se crea este signal para evitar que se puedan seguir reservando libros en el admin a pesar de ya estar en 0 la cantidad.
# # SE HACE CON 'PRE_SAVE' PARA EVITAR GUARDADO ANTES DE LA VALIDACIÓN
# def validar_creacion_reserva(sender,instance,**kwargs):
#     libro = instance.libro # Se saca el campo 'libro de la instancia, 'reserva'
#     if libro.cantidad <= 0:
#         raise Exception("No se puede realizar la reserva. Libro no disponible")    


post_save.connect(quitar_relacion_autor_libro, sender = Autor)
post_save.connect(reducir_cantidad_libro, sender = Reserva)
post_delete.connect(aumentar_cantidad_libro_delete, sender = Reserva)
#post_save.connect(aumentar_cantidad_libro_update, sender = Libro)
#pre_save.connect(validar_creacion_reserva, sender = Reserva)
    