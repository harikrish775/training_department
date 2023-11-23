# Generated by Django 4.2.6 on 2023-11-21 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='trainee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee'),
        ),
        migrations.AddField(
            model_name='notification',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer'),
        ),
    ]
