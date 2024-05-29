from django.contrib.auth.models import AbstractUser
from django.db import models
from traductor import utils

class User(AbstractUser):
    image = models.ImageField(
        verbose_name='Archivo de imagen',
        upload_to='users',
        max_length=1024,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_image_url(self):
        return utils.get_image(self.image)


