# Generated by Django 4.2.4 on 2023-09-25 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0012_contenido_image_contenido_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
