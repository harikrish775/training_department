from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from .models import Trainee,Trainer,Course,Notification,CustomUser,Department,TrainerNotification,TraineeNotification,Project,TrainerLeave,Trainee_attendence,Class_schedule,Trainer_attendence
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
import random,string
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.


def generate_password(length=6):
    # Define the characters to be used in the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password using the specified length
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

# Example: Generate a password with default length (12 characters)
# -------------------------------------------------------------------------------------

      

def loginpage(request):
    return render(request,'loginpage.html')

@login_required(login_url='loginpage')
def logoutt(request):
    logout(request)
    return redirect('loginpage')

def loginaction(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('admin')
            elif user.is_special:
                login(request,user)
                return redirect('trainerdash')
            else:
                login(request,user)
                return redirect('traineehome')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('loginpage')
    


def admin(request):
    noticount = Notification.objects.filter(is_read = False).count()
    noti = Notification.objects.filter(is_read = False)
    return render(request,'admin.html',{'noticount':noticount,'noti':noti})

def signup(request):
    co = Course.objects.all()
    dep = Department.objects.all()
    return render(request,'signup.html',{'co':co,'dep':dep})

def signupaction(request):
    
    if request.method == 'POST':
        firstname = request.POST['fname'].capitalize()
        lastname = request.POST['lname'].capitalize()
        username = request.POST['email']
        email = request.POST['email']
        contact = request.POST['contact']
        age = request.POST['age']
        gender = request.POST['gender']
        joindate = request.POST['joindate']
        course = request.POST['course']
        image = request.FILES['image']
        rr = request.POST['rrr']
        department = request.POST['department'] 
        degree = request.FILES['degree']
        propass = '123'

        if rr == 'trainee':
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email is already linked to another account')
                return redirect('signup')
            else:
                us = CustomUser.objects.create_user(first_name=firstname,password=propass,last_name=lastname,email=email,username=username,date_joined=joindate,is_special=False)
                us.save()
                te = Trainee(contact=contact,joindate=joindate,age=age,gender=gender,course_id=course,image=image,customuser=us,department_id=department,degree=degree)
                te.save()
                no = Notification.objects.create(sender=us,message=f' A new {rr} registered as {firstname} {lastname} is waiting for your approval.',trainee_id=te.id )
                no.save()
                return redirect('loginpage')
            
        elif rr == 'trainer':
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email is already linked to another account')
                return redirect('signup')
            else:
                us = CustomUser.objects.create_user(first_name=firstname,password=propass,last_name=lastname,email=email,username=username,date_joined=joindate,is_special=True)
                us.save()
                te = Trainer(contact=contact,age=age,gender=gender,joindate=joindate,course_id=course,image=image,customuser=us,department_id=department,degree=degree)
                te.save()
                no = Notification.objects.create(sender=us,message=f'A new {rr} has registered as {firstname} {lastname}.',trainer_id=te.id )
                no.save()
                return redirect('loginpage')
        
# -------------------------------------student----------------
def traineehome(request):
    return render(request,'trainee_home.html')





# --------------------------------------student end-------------------------
            

# -------------------------------admin---------------------

def notification(request):
    no = Notification.objects.all()
    return render(request,'notification.html',{'no':no})

def records(request):
    return render(request,'records.html')

def dashboard(request):
    return render(request,'dashboard.html')

def assign(request):
    teach = Trainer.objects.all()
    asign = Trainee.objects.all()
    return render(request,'assign.html',{'asign':asign,'teach':teach})

def assignaction(request,pk):
    if request.method == 'POST':
        t = request.POST['trainr']
        c = Trainee.objects.get(id=pk)
        c.trainer_id = t
        c.save()
        return redirect('assign')
    
def course(request):
    return render(request,'course.html')

def traineerecord(request):
    rec = Trainee.objects.all()
    return render(request,'trainee_record.html',{'rec':rec})

def trainerrecord(request):
    rece = Trainer.objects.all()
    return render(request,'trainer_record.html',{'rece':rece})

def traineecard(request,pk):
    card = Trainee.objects.get(id=pk)
    return render(request,'trainee_card.html',{'i':card})

def trainercard(request,pk):
    card = Trainer.objects.get(id=pk)
    return render(request,'trainer_card.html',{'i':card})

def approve(request):
    te = Notification.objects.filter(is_read=False)
    return render(request,'aprove.html',{'te':te})

def newreg(request,pk):
    b = Notification.objects.get(id=pk)
    return render(request,'new_reg.html',{'i':b})

def approveaction(request,pk):
    n = Notification.objects.get(id=pk)
    # k = CustomUser.objects.get(id=n.sender_id)
    # k.password = generate_password()
    # k.save()
    
    subject = 'Your approval has been successful'
    message = f'Hy {n.sender.first_name} {n.sender.last_name}, \n Congratulations on being a part of ALTOS family. \n Your Login Credentials : \n Username: {n.sender.email} \n Password: {n.sender.password} '
    recipient = n.sender.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
    messages.info(request,f'{n.sender.first_name}{n.sender.last_name} approved')
    return redirect('approve')


def dept(request):
    return render(request,'department.html')

def depadd(request):
    if request.method == 'POST':
        dept = request.POST['dept']
        d = Department(departmentname=dept)
        d.save()
        return redirect('admin')

def addcourse(request):
    if request.method == 'POST':
        name = request.POST['course']
        fee = request.POST['fee']
        syllabus = request.POST['syl']
        co = Course(coursename=name,coursefee=fee,syllabus=syllabus)
        co.save()
        return redirect('course')
    


# --------------------------------------admin end------------
# -----------------------------teacher-------------------------------------

def trainerhome(request):
    return render(request,'trainer_home.html')

def managetrainee(request):
    user = request.user.id
    t = Trainer.objects.get(customuser_id=user)
    rec = Trainee.objects.filter(trainer_id=t.id)
    return render(request,'managetrainee.html',{'rec':rec,'t':t})

def traineenoti(request,pk):
    if request.method == 'POST':
        message = request.POST['message']
        n = TraineeNotification(sender_id=pk,message=message,is_read=False)
        n.save()
        messages.info(request,'mail sent')
        return redirect('trainerdash')
    
def trainerdash(request):
    user = request.user.id
    t = Trainer.objects.get(customuser_id=user)
    return render(request,'trainerdash.html',{'t':t})

def trainerleave(request):
    return render(request,'trainer_leaveportal.html')

def trainerleaveapply(request):
    return render(request,'trainer_leaveapply.html')

def applyleaveaction(request):
    if request.method == 'POST':
        user = request.user.id
        tr = Trainer.objects.get(customuser_id=user)
        res = request.POST['reason']
        frm = request.POST['from']
        to = request.POST['to']
        m = TrainerLeave(from_date=frm,to_date=to,reason=res,trainer=tr)
        m.save()
        return redirect('trainerleaveapply')

def trainer_seeleave(request):
    tr = TrainerLeave.objects.all()
    return render(request,'trainer_seeleave.html',{'leave':tr})

def trainer_assignproject(request):
    return render(request,'trainer_assignproject.html')

def trainer_assignproject_action(request):
    if request.method == 'POST':
        name = request.POST['projectname']
        startdate = request.POST['sdate']
        enddate = request.POST['edate']
        f = Project(projectname=name,startdate=startdate,enddate=enddate)
        f.save()
        return render(request,'trainer_assignproject.html')

def trainer_markattendence(request):
    
    a = Trainee.objects.all()
    t_date = datetime.today().strftime('%Y-%m-%d')
    return render(request,'trainer_markattendence.html',{'aten':a,'t':t_date})

def trainer_markaction(request,pk):
    if request.method == 'POST':
        g = request.POST['tdate']
        d = Trainee_attendence.objects.filter(date=g,trainee_id=pk)
        b = request.POST['attn']
        if d.exists():
            messages.error(request,'attendence already marked')
            return redirect('trainer_markattendence')
        else:
            if b == 'present':
                c = Trainee_attendence(trainee_id=pk,attendence=True,date=g)
                c.save()
                messages.info(request,'marked')
                return redirect('trainer_markattendence')
            
            elif b == 'absent':
                c = Trainee_attendence(trainee_id=pk,attendence=False,date=g)
                c.save()
                messages.info(request,'marked')
                return redirect('trainer_markattendence')
            
            else:
                return redirect('trainer_markattendence')

def trainer_class_schedule(request):
    return render(request,'trainer_class_schedule.html')

def trainer_class_action(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        date = request.POST['date']
        link = request.POST['linkk']
        c = Class_schedule(topic=topic,date=date,link=link)
        return redirect('trainer_class_schedule')




# -----------------------------------teacher end------------------------------
