# Generated by Django 5.0.7 on 2024-09-16 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0002_alter_assessment_record'),
        ('survey', '0013_delete_assessment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Record',
        ),
    ]