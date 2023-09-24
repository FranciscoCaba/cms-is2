# Generated by Django 4.2.4 on 2023-09-24 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0009_alter_contenido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='reportado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('revision', 'En revisión'), ('rechazado', 'Rechazado'), ('publicado', 'Publicado')], default='En revisión', max_length=20),
        ),
    ]