# Generated by Django 4.2.6 on 2023-11-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0007_traineeleave'),
    ]

    operations = [
        migrations.AddField(
            model_name='traineeleave',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trainerleave',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]