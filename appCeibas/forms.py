from django import forms 

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm 
from .models import *



class FormCreateUSer(forms.ModelForm):

    class Meta:
         model = User 
         fields = (
            'username',
            'perIdentificacion',
            'perNombres',
            'perApellidos',
            'perCorreo',
            'perNumeroCelular',
            'userFoto',
            'userTipo',
         )

class FormCreatePQR(forms.ModelForm):
    class Meta:
        model=PQR
        fields=(
            'pqrDescripcion',
            'pqrConsumidor'
        )

class FormResponderPQR(forms.ModelForm):
    class Meta:
        model=PQR
        fields=(
            'pqrRespuesta',
            'pqrEstadoRespuesta'
        )

class UserPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email= self.cleaned_data.get('email')
        if not User.objects.filter(perCorreo__iexact=email, is_active=True).exists():
            raise forms.ValidationError('No hay un usuario asociado a ese correo')
        
        return email

class UserPasswordConfirmForm(SetPasswordForm):
    def clean_new_password1(self):
        password1= self.cleaned_data.get('new_password1')

        if len(password1) < 8:
            raise forms.ValidationError('La contaseña debe contener minimo 10 caracteres, y las contraseñas deben ser iguales')
        return password1