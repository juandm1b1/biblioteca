from django import forms
from .models import Autor, Libro


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
        


class LibroForm(forms.ModelForm):
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
            'fecha_publicacion': forms.SelectDateWidget(
                attrs={
                    'class': 'form-control form-row',
                }    
            )                               
        }
