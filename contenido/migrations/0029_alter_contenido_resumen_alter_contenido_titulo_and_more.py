# Generated by Django 4.2.4 on 2023-10-16 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0028_rename_razon_rechazo_contenido_nota_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='resumen',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='titulo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='versioncontenido',
            name='resumen',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='versioncontenido',
            name='titulo',
            field=models.CharField(max_length=100),
        ),
    ]
