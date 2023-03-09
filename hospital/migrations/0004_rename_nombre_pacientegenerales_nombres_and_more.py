# Generated by Django 4.1.7 on 2023-03-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_informe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pacientegenerales',
            old_name='Nombre',
            new_name='Nombres',
        ),
        migrations.AddField(
            model_name='pacientegenerales',
            name='Apellidos',
            field=models.CharField(default='SinApellido', max_length=100),
        ),
    ]