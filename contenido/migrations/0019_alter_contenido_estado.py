# Generated by Django 4.2.4 on 2023-10-02 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0018_remove_versioncontenido_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('revision', 'En revisión'), ('apublicar', 'A publicar'), ('rechazado', 'Rechazado'), ('publicado', 'Publicado')], default='En revisión', max_length=20),
        ),
    ]
