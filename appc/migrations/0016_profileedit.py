# Generated by Django 4.2.6 on 2023-11-28 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appc', '0015_traineeleave_datedifference_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileEdit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_edited', models.BooleanField(default=True)),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(null=True)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
    ]
