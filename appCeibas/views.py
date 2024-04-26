from django.shortcuts import render, reverse
from .models import *
from datetime import datetime,timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.db import transaction
import string
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import (FormView, ListView, View, CreateView, UpdateView, TemplateView)
from .forms import FormCreateUSer, FormCreatePQR, FormResponderPQR, UserPasswordResetForm, UserPasswordConfirmForm
from .models import User, PQR

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView, 
    PasswordResetCompleteView,
)
from django.core.mail import send_mail

# Create your views here.


datosSesion = {"user": None, "rutaFoto": None, "rol": None}


def error_404(request, exception):
    return render(request, '404.html', {}, status=404)


class inicio(TemplateView):
    template_name = "inicio.html"

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user=authenticate(
            perCorreo=email,
            password=password
        )
        #print(user)
        if user is not None:
            # Si el usuario existe, lo logueamos
            login(request, user)
            
            return redirect(reverse('inicio'))
        else:
            # Manejar el caso en el que la autenticación falla, podrías renderizar un mensaje de error
            # o redireccionar a una página de inicio de sesión nuevamente con un mensaje de error.
            return redirect(reverse('inicio'))

class Logout(View):
    def get(self, request, *args, **kwargs):

        logout(request)
        return HttpResponseRedirect(
            reverse(
                'inicio'
            )
        )  

class ListaEmpleados(ListView):
    template_name='listaEmpleados.html'
    model = User
    context_object_name = 'empleados'

    def get_queryset(self):
        queryset=User.objects.filter(is_superuser=False)
        return queryset


class crearEmpleados(FormView):
    template_name = 'crearEmpleado.html'
    form_class = FormCreateUSer
    success_url= reverse_lazy('lista_empleados')

    def form_valid(self, form):
        password = User.objects.generate_password()

        User.objects.create_user(
            form.cleaned_data['perCorreo'],
            password,
            True,
            perIdentificacion=form.cleaned_data['perIdentificacion'],
            perNombres=form.cleaned_data['perNombres'],
            perApellidos=form.cleaned_data['perApellidos'],
            perNumeroCelular=form.cleaned_data['perNumeroCelular'],
            userFoto=form.cleaned_data['userFoto'],
            userTipo=form.cleaned_data['userTipo']
        )

        #Envio de email
        asunto='Apertura Cuenta de Las Ceibas PQR'
        email_remitente='tb4project@gmail.com'
        mensaje = f'Bienvenido al sistema PQR Empresas públicas, su contraseña es: {password}'

        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['perCorreo'],])

        return super(crearEmpleados, self).form_valid(form)
    

class EstadoEmpleado(View):
    def post(self, request):
        user_id = request.POST.get('id')
        try:
            user = User.objects.get(id=user_id)
            # Cambiar el estado al contrario
            user.is_active = not user.is_active
            user.save()
            message = f"El estado del usuario {user.perNombres} ha sido cambiado correctamente."
            return JsonResponse({'message': message}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
    
    
class ListarPQR(ListView):
    template_name='listaPQR.html'
    context_object_name = 'pqrs'
    model = PQR

    def get_queryset(self):
        queryset = PQR.objects.filter(pqrAbogado=None)
        
        return queryset


class ListaPQRAbogado(ListView):
    template_name='listaPQRAbogado.html'
    context_object_name='pqrs'
    model= PQR 

    def get_queryset(self):
        usuario = self.request.user
        queryset = PQR.objects.filter(pqrAbogado=usuario)
        return queryset


class TomarPQRAbogado(View):
    def post(self, request):
        id_pqr = request.POST.get('id_pqr')
        id_abogado = request.POST.get('id_abogado')

        try:
            pqr = get_object_or_404(PQR, id=id_pqr)
            abogado = get_object_or_404(get_user_model(), id=id_abogado)

            pqr.pqrAbogado = abogado
            pqr.save()
            return HttpResponseRedirect(reverse('lista_pqrs_abogado'))
        except (PQR.DoesNotExist, get_user_model().DoesNotExist):
            return HttpResponseRedirect(reverse('lista_pqr'))


class CrearPQR(CreateView):
    form_class=FormCreatePQR
    template_name='crearPQR.html'
    success_url=reverse_lazy('lista_pqr')

    def form_valid(self, form):
        # Asignar el usuario activo al campo id_abogado del objeto PQR
        form.instance.pqrAsistente = self.request.user
        return super().form_valid(form)


class ResponderPQR(UpdateView):
    template_name='responderPQR.html'
    model=PQR
    form_class=FormResponderPQR
    success_url=reverse_lazy('lista_pqrs_abogado')

    def form_valid(self, form):
        form.instance.pqrEstado = False
        return super().form_valid(form)           
    
def urlValidacion(request, texto):
    """
    Esta es una funcion cuyo fin es la autenticación del usuario y su grupo, y redirige a diferentes
    plantillas HTML con un mensaje de error si la URL ingresada no es válida.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP de Django.
        texto (str): El texto que se va a validar en la URL.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza una plantilla HTML apropiada.
    """

    mensaje2 = "Nuestro sistema detecta que la ulr ingresada no es valida,por favor verifique."
    if not request.user.is_authenticated:
        return render(request, "inicio.html", {"mensaje2": mensaje2})
    if request.user.groups.filter(name='Asistente').exists():
        return render(request, "inicio.html", {"mensaje2": mensaje2})
    elif request.user.groups.filter(name='Administrador').exists():
        return render(request, "inicio.html", {"mensaje2": mensaje2})
    elif request.user.groups.filter(name='Abogado').exists():
        return render(request, "inicio.html", {"mensaje2": mensaje2})
    
    return HttpResponse("Default response")

def is_valid_url(url):
    # Implement your logic to check if the URL is valid
    # For example, you can use a regex pattern to check the URL format
    # Return True if the URL is valid, False otherwise
    return True  # Placeholder, implement your validation logic

class UserPasswordResetView(FormView):
    template_name = 'password/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(perCorreo=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # Generar token y construir la URL de restablecimiento de contraseña
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())

            # Construir la URL de restablecimiento de contraseña
            reset_link = self.request.build_absolute_uri(reverse_lazy('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))

            # Enviar correo electrónico
            subject = 'Restablecimiento de contraseña'
            message = f'Para restablecer tu contraseña, visita: {reset_link}'
            from_email = 'olortiz439@misena.edu.co'  
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            return super().form_valid(form)
        else:
            # Si el usuario no existe, mostrar un mensaje de error
            form.add_error('email', 'No se encontró ningún usuario con este correo electrónico.')
            return super().form_invalid(form)

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name='password/password_reset_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    form_class = UserPasswordConfirmForm
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        # Obtener uidb64 y token de la URL
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        
        # Decodificar uidb64 y obtener el usuario correspondiente
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            self.user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None

        # Verificar el token y el usuario
        if self.user is not None:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('Token inválido o usuario inexistente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context

class Dashboard(TemplateView):
    template_name='dashboard.html'
    
