from django.db import models

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
    autor_id = models.ManyToManyField(Autor, verbose_name='Autor(es)')
    fecha_publicacion = models.DateField('Fecha de publicación', blank=False, null=False)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now=True, auto_now_add=False)
    

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo
