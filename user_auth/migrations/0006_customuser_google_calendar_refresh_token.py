# Generated by Django 5.0 on 2024-01-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_customuser_google_calendar_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='google_calendar_refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]