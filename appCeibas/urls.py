from django.urls import path 
from .views import *

urlpatterns = [
   
    path('crear_empleado', crearEmpleados.as_view(), name='crear_empleados'),
    path('reset/password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('lista_empleados', ListaEmpleados.as_view(), name='lista_empleados'),
    path('estado_usuario', EstadoEmpleado.as_view(), name='estado_usuario'),
    path('lista_pqr', ListarPQR.as_view(), name='lista_pqr'),
    path('lista_pqr_abogado', ListaPQRAbogado.as_view(), name='lista_pqrs_abogado'),
    path('tomar_pqr_abogado', TomarPQRAbogado.as_view(), name='tomar_pqr_abogado'),
    path('crear_pqr', CrearPQR.as_view(), name='crear_pqr'),
    path('responder_pqr/<pk>', ResponderPQR.as_view(), name='responder_pqr'),
    path('logout', Logout.as_view(), name='logout'),
    path('dashboard', Dashboard.as_view(), name='dashboard')
]
