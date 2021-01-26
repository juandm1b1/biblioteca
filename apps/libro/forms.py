from django import forms
from django.core.exceptions import ValidationError
from .models import Autor, Libro, Reserva


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        exclude = ['id', 'estado','fecha_creacion']
        # Para definir etiqueta personalizada asociada a C/uno de los stributos seleccionados
        labels = {
            'nombre':'Nombres del Autor:',
            'apellido': 'Apellidos del Autor:',
            'pais': 'País del Autor:',
            'descripcion': 'Descripción:',
        }
        #Como renderizamos el campo donde vamos a escribir la información (o c/ elemento html)
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los nombres',
                    'id': 'nombres'
                }),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los apellidos',
                    'id': 'apellidos'
                }),
            'pais': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el país de origen del autor',
                    'id': 'pais'
                }),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripción',
                    'id': 'descripcion'
                })        
        }


years = []
for y in range(2020,1899,-1):
    years.append(y)

YEARS_FECHA_PUBLICACION = years


class LibroForm(forms.ModelForm):
    """ Para que al eliminar un autor, luego este no se vea al consultar o registrar libros se redefine el constructor/init
        Se accede al campo autor_id, y al ser un campo de muchos a muchos (o también FK), tiene un atributo queryset el cual se redefine.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autor_id'].queryset = Autor.objects.filter(estado=True) # Se redefine el queryset
    
    class Meta:
        model = Libro
        exclude = ['id','estado','fecha_creacion']

        labels = {
                'titulo':'Título del libro:',
                'autor_id': 'Autor(es) del libro:',
                'fecha_publicacion': 'Fecha de publicación:'                
            }
            #Como renderizamos el campo donde vamos a escribir la información (o c/ elemento html)
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el título',
                    'id': 'titulo'
                }),
            'autor_id': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                }), 
            'fecha_publicacion': forms.SelectDateWidget(years=YEARS_FECHA_PUBLICACION,
                attrs={
                    'class': 'form-control form-row',
                }    
            )                               
        }



class ReservaForm(forms.ModelForm):
    """ 
    Este form se crea para que NO aparezcan los libros No disponibles, en la lista de libros para reservar en el Admin
    Por lo tanto este ReservaForm debe ser agregado al form de Reserva del Admin
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['libro'].queryset = Libro.objects.filter(estado=True, cantidad__gte = 1) # Se redefine el queryset
    """

    model = Reserva
    fields = '__all__'

    # Otra opción: en vez de redefinir la consulta en el form, se valida cantidad de
    def clean_libro(self):
        libro = self.cleaned_data['libro'] # Cuando pase el .is_valid()
        if libro.cantidad < 1:
            raise ValidationError('No se puede reservar este libro. Deben existir unidades disponibles.')
        return libro
    

    
