from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from cms_is2 import settings
#Contenido
class Contenido(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'contenido'
        verbose_name_plural = 'contenido'
        ordering = ['-id']

    def __str__(self):
        return self.titulo
    
    def get_likes(self):
        return self.likes


#perfil de usuario

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-id']    
    
    
    def __str__(self):
        return self.user.username
    
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)