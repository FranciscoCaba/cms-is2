# Generated by Django 4.2.4 on 2023-11-14 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0031_calificacion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contenido',
            options={'permissions': [('ver_borradores', 'Ver borradores'), ('ver_rechazados', 'Ver rechazados'), ('ver_revisiones', 'Ver revisiones'), ('ver_a_publicar', 'Ver contenidos a publicar'), ('ver_kanban', 'Ver kanban'), ('ver_todos_kanban', 'Ver todos kanban'), ('puede_publicar_rechazar', 'Puede publicar o rechazar'), ('puede_editar_aceptar', 'Puede editar o aceptar'), ('ver_todos_borradores', 'Ver todos los borradores'), ('puede_publicar_no_moderada', 'Puede publicar en categoria no moderada'), ('ver_versiones', 'Ver versiones'), ('ver_todos_versiones', 'Ver todos las versiones'), ('ver_historial', 'Ver historial'), ('puede_calificar', 'Puede calificar'), ('puede_inactivar_contenido', 'Puede inactivar contenido'), ('puede_ver_estadisticas', 'Puede ver estadísticas')]},
        ),
    ]
