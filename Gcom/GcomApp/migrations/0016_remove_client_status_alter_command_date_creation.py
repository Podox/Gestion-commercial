# Generated by Django 4.2.13 on 2024-09-12 16:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GcomApp', '0015_remove_offre_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='status',
        ),
        migrations.AlterField(
            model_name='command',
            name='date_creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
