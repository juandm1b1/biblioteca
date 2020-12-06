from django import forms
#from django.contrib.auth.forms import UserCreationForm # Formulario por defecto para creación de usuario
from django.contrib.auth.forms import AuthenticationForm # Formulario por defecto para autenticación
from apps.usuario.models import Usuario


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormularioUsuario(forms.ModelForm):
    """ Formulario de registro de un usuario en la BD.
    Variables:
        - password1: contraseña
        - password2: verificación de la contraseña 
    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs= {
            'class':'form-control',
            'placeholder':'Ingrese su contraseña...',
            'id':'password1',
            'required':'required',
        }
    ))
    
    password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput(
        attrs= {
            'class':'form-control',
            'placeholder':'Ingrese nuevamente su contraseña...',
            'id':'password2',
            'required':'required',
        }
    ))
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'nombres', 'apellidos')
        widgets = {
            'email': forms.EmailInput(
                attrs= {
                    'class':'form-control',
                    'placeholder':'Correo electrónico',
                }
            ),
            'username': forms.TextInput(
                attrs= {
                    'class':'form-control',
                    'placeholder':'Ingrese su Nombre de Usuario',
                }
            ),
            'nombres': forms.TextInput(
                attrs= {
                    'class':'form-control',
                    'placeholder':'Ingrese su Nombre',
                }
            ),
            'apellidos': forms.TextInput(
                attrs= {
                    'class':'form-control',
                    'placeholder':'Ingrese sus Apellidos',
                }
            ),
        }

    # Como no hay campo contraseña en el modelo Usuario, aquí se crea una VALIDACIÖN, definiendo un método que empieza 'clean_':
    def clean_password2(self):
        """ Validación de contraseña:
        
        Método que valida que ambas contraseñas ingresadas sean iguales, esto antes de ser encriptadas y guardadas en la BD.
        Retorna la contraseña validada. 

        Excepciones:
         - ValidationError : CUando las contraseñas no son iguales muestra mensaje de error
        """
        #print('ENTRÓ A CLEAN-PASSWORD2 DE FORMS.PY')
        #print(self.cleaned_data)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            print('ENTRÓ AL IF DE FORMS.PY')
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2


    """ Se redefine/sobreescribe método save() -del módulo forms, no el de models- para guardar password.
        - commit -> significa que proceda con el registro        
    """
    def save(self, commit = True):
        #print('ENTRÓ A SAVE DE FORMS.PY')
        user = super().save(commit=False) # Cuando se cambia commit a False, no se llama directamente el save() del modelo, sino que se guarda la instancia/info que se pretende guardar
        user.set_password(self.cleaned_data['password1']) # Método set_password() que encripta las contraseñas -viene de 'AbstractBaseUser'
        if commit: # Cuando el commit pase a True durante la ejecución luego de encriptar la contraseña
            user.save()
        return user

