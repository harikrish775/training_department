from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    is_special = models.BooleanField(default=False)


class Department(models.Model):
    departmentname = models.CharField(max_length=255)

class Trainer(models.Model):
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    contact = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    joindate = models.DateField()
    image = models.ImageField(upload_to='image/')
    degree = models.FileField(upload_to='file/')
    

class Trainee(models.Model):
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.SET_NULL,null=True)
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

class TempSignup(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    joindate = models.DateField()
    image = models.ImageField(upload_to='image/')
    degree = models.FileField(upload_to='file/')
    is_special = models.BooleanField(default=False)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    

class Notification(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    person = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_approved = models.BooleanField(null=True)
    tempsignup = models.ForeignKey(TempSignup,on_delete=models.CASCADE,null=True)
    trainee =  models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    
    

class TraineeNotification(models.Model):
    sender = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    person = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    forr = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True) 
    



class TrainerNotification(models.Model):
    
    message = models.CharField(max_length=255)
    person = models.CharField(max_length=255)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    is_read = models.BooleanField(default=False)
    forr = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)



class Project(models.Model):
    projectname = models.CharField(max_length=255)
    description = models.TextField()
    startdate = models.DateField()
    enddate = models.DateField()
    status = models.BooleanField(default=False)
    file = models.FileField(upload_to='file/',null=True)
    is_delay = models.BooleanField(default=False)
    trainer = models.ForeignKey(Trainer,on_delete=models.SET_NULL,null=True)
    dateassigned = models.DateField()
    forr = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)

class SubmitedProject(models.Model):
    projectcopy = models.ForeignKey(Project,on_delete=models.SET_NULL,null=True)
    projectname = models.CharField(max_length=255)
    description = models.TextField()
    startdate = models.DateField()
    enddate = models.DateField()
    status = models.BooleanField(default=True)
    file = models.FileField(upload_to='file/',null=True)
    is_delay = models.BooleanField(default=False)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    trainee = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)
    
    

class TrainerLeave(models.Model):
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    datedifference = models.IntegerField(null=True)
    is_approved = models.BooleanField(null=True)
    is_read = models.BooleanField(default=False)

class TraineeLeave(models.Model):
    trainee = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    datedifference = models.IntegerField(null=True)
    is_approved = models.BooleanField(null=True)
    is_read = models.BooleanField(default=False)

class Class_schedule(models.Model):
    topic = models.CharField(max_length=255)
    date = models.DateField()
    link = models.CharField(max_length=255)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)

class Class_schedule(models.Model):
    topic = models.CharField(max_length=255)
    date = models.DateField()
    link = models.CharField(max_length=255)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)

class ProfileEdit(models.Model):
    is_edited = models.BooleanField(default=True)
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_approved = models.BooleanField(null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    trainee = models.ForeignKey(Trainee,on_delete=models.CASCADE,null=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=255)
    age = models.IntegerField()
    image = models.ImageField(upload_to='image/',null=True)


    
