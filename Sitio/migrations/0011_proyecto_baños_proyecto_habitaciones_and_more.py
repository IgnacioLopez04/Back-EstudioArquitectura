# Generated by Django 5.0 on 2024-01-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sitio', '0010_cliente_token_proyecto_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='baños',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='habitaciones',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='metrosCubiertos',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='metrosTotales',
            field=models.IntegerField(null=True),
        ),
    ]
