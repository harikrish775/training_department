# Generated by Django 4.2.6 on 2023-11-28 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0019_remove_trainernotification_trainer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='forr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.trainee'),
        ),
        migrations.AlterField(
            model_name='submitedproject',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
