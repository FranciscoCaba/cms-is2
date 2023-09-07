from django.db import models
from django.contrib.auth.models import Group

class CustomGroup(Group):
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Custom Group'
        verbose_name_plural = 'Custom Groups'
