# Generated by Django 5.0.7 on 2024-09-03 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0009_alter_response_assessment'),
        ('survey', '0012_alter_assessment_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Assessment',
        ),
    ]
