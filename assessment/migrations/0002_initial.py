# Generated by Django 5.0.7 on 2024-10-22 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assessment', '0001_initial'),
        ('record', '0001_initial'),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.record'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey'),
        ),
    ]
