# Generated by Django 4.2.4 on 2023-09-24 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0008_alter_contenido_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('revision', 'En revisión'), ('rechazado', 'Rechazado'), ('publicado', 'Publicado')], default='Borrador', max_length=20),
        ),
    ]
