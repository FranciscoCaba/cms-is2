# Generated by Django 4.2.4 on 2023-09-27 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0013_alter_contenido_image_alter_contenido_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='contenido/images'),
        ),
    ]
