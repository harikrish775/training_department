# Generated by Django 4.2.6 on 2023-11-23 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0009_class_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='action',
        ),
    ]