# Generated by Django 4.2.6 on 2023-11-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0005_trainernotificationstatus_traineenotificationstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainerleave',
            name='is_approved',
            field=models.BooleanField(null=True),
        ),
    ]