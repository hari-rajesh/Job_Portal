# Generated by Django 5.1 on 2024-08-25 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobApp', '0003_internship_job_application'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_details', models.TextField()),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Applied', max_length=50)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JobApp.internship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_details', models.TextField()),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Applied', max_length=50)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JobApp.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
