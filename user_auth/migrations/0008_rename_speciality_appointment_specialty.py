# Generated by Django 5.0 on 2024-01-27 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_alter_appointment_speciality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='speciality',
            new_name='specialty',
        ),
    ]
