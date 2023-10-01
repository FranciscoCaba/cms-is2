# Generated by Django 4.2.4 on 2023-09-30 15:54

import cloudinary_storage.storage
import cloudinary_storage.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0016_alter_contenido_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenido',
            name='image',
        ),
        migrations.RemoveField(
            model_name='contenido',
            name='video',
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(), upload_to='contenido/videos', validators=[cloudinary_storage.validators.validate_video])),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='contenido.contenido')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='contenido/images')),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='contenido.contenido')),
            ],
        ),
    ]