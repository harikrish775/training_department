# Generated by Django 4.2.6 on 2023-11-28 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0016_profileedit'),
    ]

    operations = [
        migrations.AddField(
            model_name='traineenotification',
            name='forr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee'),
        ),
        migrations.AddField(
            model_name='trainernotification',
            name='forr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee'),
        ),
    ]
