# Generated by Django 5.1 on 2024-08-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobApp', '0006_profile_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='domain_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='domain_name',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
    ]
