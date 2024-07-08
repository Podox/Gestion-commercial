# Generated by Django 5.0.6 on 2024-07-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GcomApp', '0003_status_client_date_creation_command_date_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='command',
            name='type_commande',
            field=models.CharField(choices=[('Prestation', 'Prestation'), ('Materiel', 'Materiel'), ('Les-deux', 'Les-deux')], default='Prestation', max_length=20),
        ),
    ]
