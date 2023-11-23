from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    is_special = models.BooleanField(default=False)

class Course(models.Model):
    coursename = models.CharField(max_length=255)
    coursefee = models.IntegerField()
    syllabus = models.FileField(upload_to='file/')

class Department(models.Model):
    departmentname = models.CharField(max_length=255)

class Trainer(models.Model):
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    joindate = models.DateField()
    image = models.ImageField(upload_to='image/')
    degree = models.FileField(upload_to='file/')

class Trainee(models.Model):
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    joindate = models.DateField()
    image = models.ImageField(upload_to='image/')
    degree = models.FileField(upload_to='file/')
    
    
class Trainee_attendence(models.Model):
    trainee = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)
    date = models.DateField()
    attendence = models.BooleanField()

class Trainer_attendence(models.Model):
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    date = models.DateField()
    attendence = models.BooleanField()

class Notification(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    person = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    trainee = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)

class TraineeNotification(models.Model):
    sender = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    person = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

class TrainerNotification(models.Model):
    sender = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    person = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

class Project(models.Model):
    projectname = models.CharField(max_length=255)
    description = models.TextField()
    startdate = models.DateField()
    enddate = models.DateField()
    status = models.BooleanField(default=False)
    action = models.BooleanField(default=False)
    file = models.FileField(upload_to='file/',null=True)
    is_delay = models.BooleanField(default=False)

class TrainerLeave(models.Model):
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)

class Class_schedule(models.Model):
    topic = models.CharField(max_length=255)
    date = models.DateField()
    link = models.CharField(max_length=255)
