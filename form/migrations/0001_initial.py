# Generated by Django 5.0.7 on 2024-10-22 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assessment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FormSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.form')),
            ],
        ),
        migrations.CreateModel(
            name='InputField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.formsection')),
            ],
        ),
        migrations.CreateModel(
            name='InputTextField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.form')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fields', models.JSONField()),
                ('assessment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assessment.assessment')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.form')),
            ],
        ),
        migrations.CreateModel(
            name='TextFieldResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.inputtextfield')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.response')),
            ],
        ),
    ]
