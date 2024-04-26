from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import UserManager
from django.contrib.auth import get_user_model

# Create your models here.
estadoEmpleados = [
    ('Activo', 'Activo'), ('Inactivo', 'Inactivo')
]
tipoUsuario = [
    ('Asistente comercial', 'Asistente comercial'), ('Abogado',
                             'Abogado'), ('Administrativo', 'Administrativo')
]


class Persona(models.Model):
    perIdentificacion = models.CharField(
        max_length=10, unique=True, null=True, blank=True, db_comment="Identificacion de la persona")
    perNombres = models.CharField(
        max_length=70, null=True, db_comment="Nombres de la persona")
    perApellidos = models.CharField(
        max_length=70, null=True, db_comment="Apellidos de la persona")
    perCorreo = models.CharField(
        max_length=70, unique=True, db_comment="Correo de la persona")
    perNumeroCelular = models.CharField(
        max_length=10, unique=True, null=True, blank=True, db_comment="Numero de celular de la persona")
    
    class Meta:
        abstract = True
    
    """ def __str__(self):
        return f"Identificacion:{self.perIdentificacion} -Nombres: {self.perNombres} -Apellidos:{self.perApellidos} -Correo:{self.perCorreo} -Celular:{self.perNumeroCelular}" """


class User(Persona, AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50)  # Fixed max_length value
    userFoto = models.FileField(
        upload_to="fotos/", null=True, blank=True, db_comment="Foto del Usuario")
    userTipo = models.CharField(
        max_length=20, choices=tipoUsuario, db_comment="Nombre Tipo de usuario")
    fechaHoraCreacion = models.DateTimeField(
        auto_now_add=True, db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(
        auto_now=True, db_comment="Fecha y hora última actualización")
    userEstado = models.CharField(choices=estadoEmpleados, max_length=20, default=True)  # Fixed max_length value

    USERNAME_FIELD = 'perCorreo'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return  str(self.id) + self.username


class Consumidor(Persona):
    
    def __str__(self):
        return f"Consumidor: {self.perNombres} {self.perApellidos}"


class PQR(models.Model):
    pqrFecha = models.DateTimeField(
        auto_now_add=True, db_comment="Fecha y hora del registro"   )
    pqrDescripcion = models.TextField(
        max_length=600,  null=True, db_comment="Descripcion del problema")
    pqrRespuesta = models.TextField(
        max_length=600,  null=True, blank=True, db_comment="Descripcion del problema")
    pqrConsumidor = models.ForeignKey(
        Consumidor, on_delete=models.PROTECT, db_comment="Hace relación a la persona FK")
    pqrAsistente = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='pqr_asistentes')
    pqrAbogado = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='pqr_abogados', null=True, blank=True)
    pqrEstadoRespuesta = models.BooleanField(default=False)
    pqrEstado = models.BooleanField(default=True)

    def __str__(self):
        return f"Consumidor: {self.pqrConsumidor.perNombres} {self.pqrConsumidor.perApellidos} -Identificacion:{str(self.pqrConsumidor.perIdentificacion)}"