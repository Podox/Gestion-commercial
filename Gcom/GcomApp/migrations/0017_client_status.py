# Generated by Django 4.2.13 on 2024-09-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GcomApp', '0016_remove_client_status_alter_command_date_creation'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='status',
            field=models.ManyToManyField(related_name='clients', to='GcomApp.status'),
        ),
    ]
