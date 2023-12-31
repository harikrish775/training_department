# Generated by Django 4.2.6 on 2023-11-30 06:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_special', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursename', models.CharField(max_length=255)),
                ('coursefee', models.IntegerField()),
                ('syllabus', models.FileField(upload_to='file/')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentname', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('file', models.FileField(null=True, upload_to='file/')),
                ('is_delay', models.BooleanField(default=False)),
                ('dateassigned', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('joindate', models.DateField()),
                ('image', models.ImageField(upload_to='image/')),
                ('degree', models.FileField(upload_to='file/')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.course')),
                ('customuser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.department')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('joindate', models.DateField()),
                ('image', models.ImageField(upload_to='image/')),
                ('degree', models.FileField(upload_to='file/')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.course')),
                ('customuser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.department')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerNotificationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('person', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.department')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('person', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.department')),
                ('forr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('reason', models.TextField()),
                ('datedifference', models.IntegerField(null=True)),
                ('is_approved', models.BooleanField(null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer_attendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('attendence', models.BooleanField()),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='TraineeNotificationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('person', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='TraineeNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('person', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('forr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='TraineeLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('reason', models.TextField()),
                ('datedifference', models.IntegerField(null=True)),
                ('is_approved', models.BooleanField(null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee')),
            ],
        ),
        migrations.CreateModel(
            name='Trainee_attendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('attendence', models.BooleanField()),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee')),
            ],
        ),
        migrations.AddField(
            model_name='trainee',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.trainer'),
        ),
        migrations.CreateModel(
            name='TempSignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('joindate', models.DateField()),
                ('image', models.ImageField(upload_to='image/')),
                ('degree', models.FileField(upload_to='file/')),
                ('is_special', models.BooleanField(default=False)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.course')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.department')),
            ],
        ),
        migrations.CreateModel(
            name='SubmitedProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('file', models.FileField(null=True, upload_to='file/')),
                ('is_delay', models.BooleanField(default=False)),
                ('projectcopy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.project')),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='forr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee'),
        ),
        migrations.AddField(
            model_name='project',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appc.trainer'),
        ),
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
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('person', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(null=True)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tempsignup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.tempsignup')),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainee')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Class_schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('link', models.CharField(max_length=255)),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appc.trainer')),
            ],
        ),
    ]
