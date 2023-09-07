from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Contenido(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario', verbose_name='Usuario')
    titulo = models.CharField(max_length=100)
    descripcion = RichTextField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo
    