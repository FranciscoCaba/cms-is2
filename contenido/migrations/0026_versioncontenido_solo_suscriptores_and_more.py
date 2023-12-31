# Generated by Django 4.2.4 on 2023-10-02 14:35

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0025_alter_contenido_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='versioncontenido',
            name='solo_suscriptores',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='versioncontenido',
            name='descripcion',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
    ]
