# Generated by Django 5.0.7 on 2024-08-28 21:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_rename_email_temp_survey_email_template'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(on_delete=models.SET(''), to=settings.AUTH_USER_MODEL),
        ),
    ]
