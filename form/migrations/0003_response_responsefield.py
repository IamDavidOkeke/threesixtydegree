# Generated by Django 5.0.7 on 2024-08-08 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0002_alter_inputfield_section_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.form')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500)),
                ('inputField_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.inputfield')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.response')),
            ],
        ),
    ]
