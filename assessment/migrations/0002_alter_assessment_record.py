# Generated by Django 5.0.7 on 2024-09-16 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.record'),
        ),
    ]
