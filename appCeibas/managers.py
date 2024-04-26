from django.db import models
from django.contrib.auth.models import BaseUserManager

import random
import string


class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, perCorreo, password, is_staff, is_active, is_superuser, **extra_fields):

        user=self.model(
            perCorreo=perCorreo,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **extra_fields,
        )
        #Se hace el manejo de la contraseña
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, perCorreo, password=None, **extra_fields):

        return self._create_user(perCorreo,  password, True, True, True, **extra_fields)

    
    def create_user(self, perCorreo, password=None, is_active=False, **extra_fields):

        return self._create_user(perCorreo, password, False, is_active, False, **extra_fields)

    
    def generate_password(self, size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
        