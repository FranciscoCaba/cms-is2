# Generated by Django 4.2.4 on 2023-10-02 05:49

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0023_merge_20231002_0549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contenido',
            options={'permissions': [('ver_borradores', 'Ver borradores'), ('ver_rechazados', 'Ver rechazados'), ('ver_revisiones', 'Ver revisiones'), ('ver_a_publicar', 'Ver contenidos a publicar'), ('ver_kanban', 'Ver kanban'), ('ver_todos_kanban', 'Ver todos kanban'), ('puede_publicar_rechazar', 'Puede publicar o rechazar'), ('ver_todos_borradores', 'Ver todos los borradores'), ('puede_publicar_no_moderada', 'Puede publicar en categoria no moderada')]},
        ),
        migrations.AlterField(
            model_name='contenido',
            name='descripcion',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
    ]