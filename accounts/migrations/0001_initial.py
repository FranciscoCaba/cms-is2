# Generated by Django 4.2.4 on 2023-08-25 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='user/usuario_defecto,jpg', upload_to='users/', verbose_name='Imagen de perfil')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Direccion')),
                ('localidad', models.CharField(blank=True, max_length=150, null=True, verbose_name='localidad')),
                ('telephone', models.CharField(blank=True, max_length=150, null=True, verbose_name='telefono')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
                'ordering': ['-id'],
            },
        ),
    ]
