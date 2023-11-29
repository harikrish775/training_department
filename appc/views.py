from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from .models import Trainee,Trainer,Course,Notification,CustomUser,Department,TrainerNotification,TraineeNotification,Project,TrainerLeave,Trainee_attendence,Class_schedule,Trainer_attendence,TempSignup,SubmitedProject,TraineeNotificationStatus,TrainerNotificationStatus,TraineeLeave,ProfileEdit
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
import random,string
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime,date,timedelta
import os
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash

# Create your views here.


def generate_password(length=6):
    # Define the characters to be used in the password
    # characters = string.ascii_letters + string.digits + string.punctuation
    characters = string.digits + string.digits + string.digits

    # Generate a random password using the specified length
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

# Example: Generate a password with default length (12 characters)
# -------------------------------------------------------------------------------------

@login_required(login_url='loginpage')
def trainer_update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if request.user.is_authenticated:
            if request.user.check_password(current_password):
            
                if new_password == confirm_new_password:
                    
                    request.user.set_password(new_password)
                    request.user.save()

                    update_session_auth_hash(request, request.user)

                    error = 'no'
                    h = Trainer.objects.get(customuser_id=request.user.id)
                    return render(request,'trainer_update_password.html',{'error':error,'t':h})
                else:
                    error = 'yes'
                    h = Trainer.objects.get(customuser_id=request.user.id)
                    return render(request,'trainer_update_password.html',{'error':error,'t':h})
            else:
                error = 'yes'
                h = Trainer.objects.get(customuser_id=request.user.id)
                return render(request,'trainer_update_password.html',{'error':error,'t':h})

    return render(request, 'trainer_update_password.html')

@login_required(login_url='loginpage')
def trainee_update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if request.user.is_authenticated:
            if request.user.check_password(current_password):
            
                if new_password == confirm_new_password:
                    
                    request.user.set_password(new_password)
                    request.user.save()

                    update_session_auth_hash(request, request.user)

                    error = 'no'
                    h = Trainee.objects.get(customuser_id=request.user.id)
                    return render(request,'trainee_update_password.html',{'error':error,'t':h})
                else:
                    error = 'yes'
                    h = Trainee.objects.get(customuser_id=request.user.id)
                    return render(request,'trainee_update_password.html',{'error':error,'t':h})
                    
            else:
                error = 'yes'
                h = Trainee.objects.get(customuser_id=request.user.id)
                return render(request,'trainee_update_password.html',{'error':error,'t':h})

    return render(request, 'trainee_update_password.html')




#----------------------------------------------------------------------------------

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
                return redirect('dashboard')
            elif user.is_special:
                login(request,user)
                return redirect('trainerdash')
            else:
                login(request,user)
                return redirect('trainee_dash')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('loginpage')
    

@login_required(login_url='loginpage')
def admin(request):
    noticount = Notification.objects.filter(is_read = False).count()
    noti = Notification.objects.filter(is_read = False)
    return render(request,'dashboard.html',{'noticount':noticount,'noti':noti})

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
        image = request.FILES['image']
        rr = request.POST['rrr']
        degree = request.FILES['degree']
        department = request.POST['department']
        propass = '123'

        if rr == 'trainee':
                te = TempSignup(first_name=firstname,last_name=lastname,username=username,email=email,password=propass,contact=contact,joindate=joindate,age=age,gender=gender,image=image,degree=degree,department_id=department)
                te.save()
                no = Notification(message=f' A new {rr} registered as {firstname} {lastname} is waiting for your approval.',tempsignup_id=te.id )
                no.save()
                return redirect('loginpage')
            
        elif rr == 'trainer':
                te = TempSignup(first_name=firstname,last_name=lastname,username=username,email=email,password=propass,contact=contact,joindate=joindate,age=age,gender=gender,image=image,degree=degree,is_special=True,department_id=department)
                te.save()
                no = Notification.objects.create(message=f'A new {rr} has registered as {firstname} {lastname}.',tempsignup_id=te.id )
                no.save()
                return redirect('loginpage')
        










# -------------------------------------student----------------












@login_required(login_url='loginpage')
def trainee_dash(request):
    
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    n = TraineeNotification.objects.filter(is_read=False).count()
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    return render(request,'trainee_dash.html',{'count':n,'co':co,'t':fg})

@login_required(login_url='loginpage')
def trainee_inbox(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False,forr_id = fg.id).count()
    dd = TraineeNotification.objects.filter(forr_id = fg.id)
    return render(request,'trainee_inbox.html',{'count':n,'co':co,'dd':dd})

@login_required(login_url='loginpage')
def trainee_markasread(request,pk):
    m = TraineeNotification.objects.get(id=pk)
    m.is_read = True
    m.save()
    return redirect('trainee_inbox')

@login_required(login_url='loginpage')
def trainee_project(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    
    return render(request,'trainee_project.html',{'count':n,'co':co})

@login_required(login_url='loginpage')
def assignedtask(request):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()

    
    p = Project.objects.filter(trainer_id=fg.trainer,forr_id=fg)
    sp = SubmitedProject.objects.filter(trainer_id=fg.trainer)
                
    return render(request,'assignedtask.html',{'v':p,'sp':sp,'co':co,'count':n,'fg':fg})

@login_required(login_url='loginpage')
def submittask(request,pk):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()

    m = Project.objects.get(id=pk)
    return render(request,'submittask.html',{'m':m,'co':co,'count':n})

@login_required(login_url='loginpage')
def submittaskaction(request,pk):
    g = Project.objects.get(id=pk)
    if request.method == 'POST':
        trainee = Trainee.objects.get(customuser_id=request.user.id)
        description = request.POST['des']
        file = request.FILES['docc']
        status = True
        today = date.today()
        g.status = True
        g.save()
       
        if today > g.enddate:
            h = SubmitedProject(projectcopy_id=pk,projectname=g.projectname,startdate=g.startdate,enddate=g.enddate,description=description,status=status,file=file,trainee_id=trainee.id,trainer_id=g.trainer_id,is_delay=True)
            h.save()
            return redirect('trainee_project')
        else:
            h = SubmitedProject(projectcopy_id=pk,projectname=g.projectname,startdate=g.startdate,enddate=g.enddate,description=description,status=status,file=file,trainer_id=g.trainer_id,trainee_id=trainee.id)
            h.save()
            return redirect('trainee_project')
        
@login_required(login_url='loginpage')
def completedtask(request):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    h = SubmitedProject.objects.filter(status=True,trainee_id=fg.id)
    return render(request,'completedtask.html',{'h':h,'co':co,'count':n})


@login_required(login_url='loginpage')
def trainee_class(request):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    trainee = Trainee.objects.get(customuser_id=request.user.id)
    t = Class_schedule.objects.filter(date=today,trainer_id=trainee.trainer)
    u = Class_schedule.objects.filter(date__gt=today,trainer_id=trainee.trainer)
    f = Class_schedule.objects.filter(date__lt=today,trainer_id=trainee.trainer)
    return render(request,'trainee_class.html',{'t':t,'u':u,'f':f,'co':co,'count':n})    

@login_required(login_url='loginpage')
def trainee_attendence(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    return render(request,'trainee_attendence.html',{'count':n,'co':co})

@login_required(login_url='loginpage')
def trainee_viewattendence(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    if request.method == 'POST':
        user = request.user.id
        c = Trainee.objects.get(customuser_id=user)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        s = Trainee_attendence.objects.filter(trainee_id=c.id,date__range=(a,b)).order_by(sort_param)
        return render(request,'trainee_viewattendence.html',{'s':s,'count':n,'co':co})


@login_required(login_url='loginpage')
def trainee_applyleave(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    return render(request,'trainee_applyleave.html',{'count':n,'co':co})

@login_required(login_url='loginpage')
def trainee_applyleaveaction(request):
    if request.method == 'POST':
        user = request.user.id
        tr = Trainee.objects.get(customuser_id=user)
        res = request.POST['reason']
        frm = request.POST['from']
        to = request.POST['to']
        m = TraineeLeave(from_date=frm,to_date=to,reason=res,trainee=tr)
        m.save()
        return redirect('trainee_applyleave')

@login_required(login_url='loginpage')
def trainee_editprofile(request):
    t = Trainee.objects.get(customuser_id=request.user.id)
    return render(request,'trainee_editprofile.html',{'t':t})

@login_required(login_url='loginpage')
def trainee_update(request,pk):
    t = Trainee.objects.get(id=pk)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        contact = request.POST['contact']
        age = request.POST['age']
        if len(request.FILES) != 0:
            image = request.FILES['image']
        else:
            image = t.image
        p = ProfileEdit(sender=t.customuser,message=f'{t.customuser.first_name} {t.customuser.last_name} with email "{t.customuser.email}" has made some changes to their profile',is_read=False,is_approved=None,is_edited=True,firstname=fname,lastname=lname,email=email,contact=contact,age=age,image=image,trainee_id=t.id)
        p.save()
        error = 'no'
        return render(request,'trainee_dash.html',{'p':p,'error':error,'t':t})



# --------------------------------------student end-------------------------
















# -------------------------------admin---------------------














@login_required(login_url='loginpage')
def notification(request):
    co = Notification.objects.filter(is_read=False).count()
    no1 = Notification.objects.filter(is_read=False)
    no = Notification.objects.all()
    return render(request,'notification.html',{'no':no,'ncount':co,'noti':no1})

@login_required(login_url='loginpage')
def admin_sendmail(request):
    if request.method == 'POST':
        todeptrainers = request.POST['todeptrainers']
        if todeptrainers == 'all':
            mess = request.POST['message']
            tt = Trainer.objects.all()
            for i in tt:
                h = TrainerNotification(message=mess,forr_id=i.id)
                h.save()
        
        else:
            mess = request.POST['message']
            tt = Trainer.objects.filter(department_id=todeptrainers)
            for i in tt:
                h = TrainerNotification(message=mess,department_id=todeptrainers)
                h.save()

        return redirect('dashboard')
    
@login_required(login_url='loginpage')
def records(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'records.html',{'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def dashboard(request):
    b = TrainerLeave.objects.filter(is_read=False).count()
    c = TraineeLeave.objects.filter(is_read=False).count()
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    po = ProfileEdit.objects.filter(is_approved='').count()
    e = Trainee.objects.all().count()
    r = Trainer.objects.all().count()
    dep = Department.objects.all()
    ko = co + po
    return render(request,'dashboard.html',{'dep':dep,'ecount':e,'rcount':r,'ncount':co,'noti':no,'b':b,'c':c,'po':po,'ko':ko})

@login_required(login_url='loginpage')
def assign(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    teach = Trainer.objects.all()
    asign = Trainee.objects.all()
    return render(request,'assign.html',{'asign':asign,'teach':teach,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def assignaction(request,pk):
    teach = Trainer.objects.all()
    asign = Trainee.objects.all()
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    if request.method == 'POST':
        if 'trainr' in request.POST :
            t = request.POST['trainr']
        else:
            t = ''

    c = Trainee.objects.get(id=pk)
    c.trainer_id = t
    c.save()
    return render(request,'assign.html',{'asign':asign,'teach':teach,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def course(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'course.html',{'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def traineerecord(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    rec = Trainee.objects.all()
    return render(request,'trainee_record.html',{'rec':rec,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def trainerrecord(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    rece = Trainer.objects.all()
    return render(request,'trainer_record.html',{'rece':rece,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def traineecard(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    card = Trainee.objects.get(id=pk)
    return render(request,'trainee_card.html',{'i':card,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def trainercard(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    card = Trainer.objects.get(id=pk)
    return render(request,'trainer_card.html',{'i':card,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def approve(request):
    
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    te = Notification.objects.all()
    edit = ProfileEdit.objects.all()
    return render(request,'aprove.html',{'te':te,'ncount':co,'noti':no,'edit':edit})

@login_required(login_url='loginpage')
def newreg(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    b = Notification.objects.get(id=pk)
    return render(request,'new_reg.html',{'i':b,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def approveaction(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    n = Notification.objects.get(id=pk)
    
    if n.tempsignup.is_special :
        trainer = TempSignup.objects.get(id=n.tempsignup_id)
        if CustomUser.objects.filter(email=trainer.email).exists():
            error = 'yes'
        else:
            # passs = generate_password()
            passs = '123'
            userr = CustomUser.objects.create_user(first_name=trainer.first_name,last_name=trainer.last_name,email=trainer.email,username=trainer.username,password=passs,is_special=trainer.is_special,date_joined=trainer.joindate)
            userr.save()
            approved_trainer = Trainer(contact=trainer.contact,age=trainer.age,gender=trainer.gender,joindate=trainer.joindate,image=trainer.image,customuser=userr,degree=trainer.degree,department_id=trainer.department.id)
            approved_trainer.save()
            
            n.is_read = True
            n.is_approved = True
            n.save()
            n.trainer_id = approved_trainer
            n.sender = userr
            n.save()

            subject = 'Your approval has been successful'
            message = f'Hy {n.sender.first_name} {n.sender.last_name}, \n Congratulations on being a part of ALTOS family. \n Your Login Credentials : \n Username: {n.sender.email} \n Password: {passs} '
            recipient = n.sender.email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            messages.info(request,f'{n.sender.first_name}{n.sender.last_name} has been approved')
            return redirect('approve')
        
    
    else:
        trainee = TempSignup.objects.get(id=n.tempsignup_id)
        if CustomUser.objects.filter(email=trainee.email).exists():
            error = 'yes'
        else:
            # passs = str(random.randint(123421,897654))
            # passs = generate_password()
            passs = '123'
            userr = CustomUser.objects.create_user(first_name=trainee.first_name,last_name=trainee.last_name,email=trainee.email,username=trainee.username,password=passs,is_special=trainee.is_special,date_joined=trainee.joindate)
            userr.save()
            approved_trainee = Trainee(contact=trainee.contact,age=trainee.age,gender=trainee.gender,joindate=trainee.joindate,image=trainee.image,customuser=userr,degree=trainee.degree,department_id=trainee.department.id)
            approved_trainee.save()
            n.trainee_id = approved_trainee
            n.sender = userr
            n.is_read = True
            n.is_approved = True
            n.save()

            subject = 'Your approval has been successful'
            message = f'Hy {n.sender.first_name} {n.sender.last_name}, \n Congratulations on being a part of ALTOS family. \n Your Login Credentials : \n Username: {n.sender.email} \n Password: {passs} '
            recipient = n.sender.email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return redirect('approve')

@login_required(login_url='loginpage')
def disapproveaction(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    n = Notification.objects.get(id=pk)
    n.is_read = True
    n.is_approved = False
    n.save()
    return redirect('approve')

@login_required(login_url='loginpage')
def dept(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    dep = Department.objects.all()
    return render(request,'department.html',{'ncount':co,'noti':no,'dep':dep})

@login_required(login_url='loginpage')
def depadd(request):
    if request.method == 'POST':
        dept = request.POST['dept']
        if dept == '':
            error='yes'
        else:
            
            d = Department(departmentname=dept)
            d.save()
            error = 'no'
        return render(request,'department.html',{'error':error})
    
@login_required(login_url='loginpage')
def deletedepp(request,pk):
    d = Department.objects.get(id=pk)
    d.delete()
    error = 'del'
    dep = Department.objects.all()
    return render(request,'department.html',{'error':error,'dep':dep})

@login_required(login_url='loginpage')
def addcourse(request):
    if request.method == 'POST':
        name = request.POST['course']
        fee = request.POST['fee']
        syllabus = request.POST['syl']
        co = Course(coursename=name,coursefee=fee,syllabus=syllabus)
        co.save()
        return redirect('course')

@login_required(login_url='loginpage')
def trainer_attendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'trainer_attendence.html',{'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def admin_mark_trainerattendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    ho = Trainer.objects.all()
    t_date = datetime.today().strftime('%Y-%m-%d')
    return render(request,'admin_mark_trainerattendence.html',{'ho':ho,'t':t_date,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def admin_mark_trainerattendence_action(request,pk):
    if request.method == 'POST':
        g = request.POST['tdate']
        d = Trainer_attendence.objects.filter(date=g,trainer_id=pk)
        b = request.POST['attn']
        if d.exists():
            error = 'yes'
            return render(request,'admin_mark_trainerattendence.html',{'error':error})

        else:
            if b == 'present':
                c = Trainer_attendence(trainer_id=pk,attendence=True,date=g)
                c.save()
                error = 'no'
                return render(request,'admin_mark_trainerattendence.html',{'error':error})
            
            elif b == 'absent':
                c = Trainer_attendence(trainer_id=pk,attendence=False,date=g)
                c.save()
                error='no'
                return render(request,'admin_mark_trainerattendence.html',{'error':error})
            
            else:
                return redirect('admin_mark_trainerattendence')

@login_required(login_url='loginpage')
def admin_view_trainerattendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    tr = Trainer.objects.all()
    return render(request,'admin_view_trainerattendence.html',{'tr':tr,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def admin_view_trainerattendence_action(request):
    if request.method == 'POST':
        l = request.POST['trid']
        c = Trainer.objects.get(id=l)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        s = Trainer_attendence.objects.filter(trainer_id=c.id,date__range=(a,b)).order_by(sort_param)
        return render(request,'admin_show_trainerattendence.html',{'s':s,'c':c,'a':a,'b':b})
    
@login_required(login_url='loginpage')  
def admin_show_trainerattendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'admin_show_trainerattendence.html',{'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def admin_view_trainee_attendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    s = Trainee.objects.all()
    return render(request,'admin_view_trainee_attendence.html',{'s':s,'ncount':co,'noti':no})

@login_required(login_url='loginpage')
def admin_view_trainee_attendence_action(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    if request.method == 'POST':
        l = request.POST['trrid']
        c = Trainee.objects.get(id=l)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        ss = Trainee_attendence.objects.filter(trainee_id=c.id,date__range=(a,b)).order_by(sort_param)
        return render(request,'admin_show_trainee_attendence.html',{'ss':ss,'c':c,'ncount':co,'noti':no,'a':a,'b':b})

@login_required(login_url='loginpage')
def admin_review_attendence(request):
    a = TrainerLeave.objects.all()
    b = TraineeLeave.objects.all()
    for i in a :
        datedifference = i.to_date - i.from_date
        i.datedifference=datedifference.days
        i.save()
    for j in b :
        datedifference = j.to_date - j.from_date
        j.datedifference=datedifference.days
        j.save()
    return render(request,'admin_review_attendence.html',{'leave':a,'bleave':b})

@login_required(login_url='loginpage')
def admin_approve_leave(request,pk):
    a = TrainerLeave.objects.get(id=pk)
    a.is_approved = True
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')

@login_required(login_url='loginpage')
def admin_reject_leave(request,pk):
    a = TrainerLeave.objects.get(id=pk)
    a.is_approved = False
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')

@login_required(login_url='loginpage')
def admin_approve_leave_trainee(request,pk):
    a = TraineeLeave.objects.get(id=pk)
    a.is_approved = True
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')

@login_required(login_url='loginpage')
def admin_reject_leave_trainee(request,pk):
    a = TraineeLeave.objects.get(id=pk)
    a.is_approved = False
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')
    
@login_required(login_url='loginpage')
def admin_remove_trainee(request,pk):
    g = Trainee.objects.get(id=pk)
    f = CustomUser.objects.get(id=g.customuser_id)
    f.delete()
    g.delete()
    
    return redirect('traineerecord')

@login_required(login_url='loginpage')
def admin_remove_trainer(request,pk):
    g = Trainer.objects.get(id=pk)
    f = CustomUser.objects.get(id=g.customuser_id)
    f.delete()
    g.delete()
    
    return redirect('trainerrecord')

@login_required(login_url='loginpage')
def assign_department(request):
    return render(request,'assign_department.html')

@login_required(login_url='loginpage')
def admin_assign_department(request):
    d = Department.objects.all()
    train = Trainer.objects.all()
    return render(request,'admin_assign_department.html',{'train':train,'dep':d})

@login_required(login_url='loginpage')
def admin_assign_department_action(request,pk):
    if request.method == 'POST':
        ff = request.POST['depart']
        trainer = Trainer.objects.get(id=pk)
        trainer.department_id=ff
        trainer.save()
        return redirect('admin_assign_department')

@login_required(login_url='loginpage')
def admin_assign_dep_trainee(request):
    d = Department.objects.all()
    train = Trainee.objects.all()
    return render(request,'admin_assign_dep_trainee.html',{'train':train,'dep':d})

@login_required(login_url='loginpage')
def admin_assign_dep_trainee_action(request,pk):
    if request.method == 'POST':
        ff = request.POST['depart']
        trainee = Trainee.objects.get(id=pk)
        trainee.department_id=ff
        trainee.save()
        return redirect('admin_assign_dep_trainee')

@login_required(login_url='loginpage')
def approvechange(request,pk):
    pp = ProfileEdit.objects.get(id=pk)
    pp.is_approved = True
    pp.save()
    g = pp.sender
    if pp.trainee_id is None and pp.trainer_id is not None:
        tt = Trainer.objects.get(customuser_id=g)
        nn = TrainerNotification(forr_id=tt.id,is_read=False,message=f'Your changes has been APPROVED')
        nn.save()
    elif pp.trainer_id is None and pp.trainee_id is not None:
        tt = Trainee.objects.get(customuser_id=g)
        nn = TraineeNotification(forr_id=tt.id,is_read=False,message=f'Your changes has been APPROVED')
        nn.save()
    
    tt.customuser.first_name = pp.firstname
    tt.customuser.last_name = pp.lastname
    tt.customuser.email = pp.email
    tt.contact = pp.contact
    tt.age = pp.age
    tt.image = pp.image
    tt.save()
    
    return redirect('approve')

@login_required(login_url='loginpage')
def rejectchange(request,pk):
    pp = ProfileEdit.objects.get(id=pk)
    pp.is_approved = False
    pp.save()
    g = pp.sender
    if pp.trainee_id is None and pp.trainer_id is not None :
        tt = Trainer.objects.get(customuser_id=g)
        nn = TrainerNotification(forr_id=tt.id,is_read=False,message=f'Your changes has been REJECTED')
        nn.save()
        return redirect('approve')
    elif pp.trainee_id is not None and pp.trainer_id is None :
        tt = Trainee.objects.get(customuser_id=g)
        nn = TraineeNotification(forr_id=tt.id,is_read=False,message=f'Your changes has been REJECTED')
        nn.save()
        return redirect('approve')
    
    


@login_required(login_url='loginpage')
def admin_see_changes(request,pk):
    ppp = ProfileEdit.objects.get(id=pk)
    return render(request,'admin_see_changes.html',{'i':ppp})




# --------------------------------------admin end------------






















# -----------------------------teacher-------------------------------------
@login_required(login_url='loginpage')
def trainerhome(request):
    return render(request,'trainer_home.html')

@login_required(login_url='loginpage')
def managetrainee(request):
    user = request.user.id
    t = Trainer.objects.get(customuser_id=user)
    rec = Trainee.objects.filter(trainer_id=t.id)
    return render(request,'managetrainee.html',{'rec':rec,'t':t})

@login_required(login_url='loginpage')
def traineenoti(request,pk):
    if request.method == 'POST':
        message = request.POST['message']
        n = TraineeNotification(sender_id=pk,message=message,is_read=False)
        n.save()
        messages.info(request,'mail sent')
        return redirect('trainerdash') #-------------------------------------------------------------------------mail for trainee

@login_required(login_url='loginpage')   
def trainerdash(request):
    user = request.user.id
    t = Trainer.objects.get(customuser_id=user)
    count = TrainerNotification.objects.filter(forr_id = t.id,is_read=False).count()
    return render(request,'trainerdash.html',{'t':t,'count':count})

@login_required(login_url='loginpage')
def trainerleave(request):
    return render(request,'trainer_leaveportal.html')

@login_required(login_url='loginpage')
def trainerleaveapply(request):
    return render(request,'trainer_leaveapply.html')

@login_required(login_url='loginpage')
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

@login_required(login_url='loginpage')
def trainer_seeleave(request):
    user = request.user.id
    f = Trainer.objects.get(customuser_id=user)
    tr = TrainerLeave.objects.filter(trainer_id=f.id)
    return render(request,'trainer_seeleave.html',{'leave':tr})

@login_required(login_url='loginpage')
def trainer_assignproject(request):
    
    return render(request,'trainer_assignproject.html')

@login_required(login_url='loginpage')
def trainer_assignproject_action(request):
    if request.method == 'POST':
        name = request.POST['projectname']
        startdate = request.POST['sdate']
        enddate = request.POST['edate']
        today = date.today()
        
        trainr = Trainer.objects.get(customuser_id=request.user.id)
        trainee = Trainee.objects.filter(trainer_id=trainr.id)
        for i in trainee:
            f = Project(projectname=name,startdate=startdate,enddate=enddate,dateassigned=today,trainer_id=trainr.id,forr_id=i.id)
            f.save()
            error = 'no'
        return render(request,'trainer_assignproject.html',{'error':error})

@login_required(login_url='loginpage')
def trainer_markattendence(request):
    us = Trainer.objects.get(customuser_id=request.user.id)
    a = Trainee.objects.filter(trainer_id=us.id)
    t_date = datetime.today().strftime('%Y-%m-%d')
    return render(request,'trainer_markattendence.html',{'aten':a,'t':t_date})

@login_required(login_url='loginpage')
def trainer_markaction(request,pk):
    if request.method == 'POST':
        g = request.POST['tdate']
        d = Trainee_attendence.objects.filter(date=g,trainee_id=pk)
        b = request.POST['attn']
        if d.exists():
            error = 'yes'
            us = Trainer.objects.get(customuser_id=request.user.id)
            a = Trainee.objects.filter(trainer_id=us.id)
            t_date = datetime.today().strftime('%Y-%m-%d')
            return render(request,'trainer_markattendence.html',{'error':error,'aten':a,'t':t_date})
        else:
            if b == 'present':
                c = Trainee_attendence(trainee_id=pk,attendence=True,date=g)
                c.save()
                error = 'no'
                us = Trainer.objects.get(customuser_id=request.user.id)
                a = Trainee.objects.filter(trainer_id=us.id)
                t_date = datetime.today().strftime('%Y-%m-%d')
                return render(request,'trainer_markattendence.html',{'error':error,'aten':a,'t':t_date})
            
            elif b == 'absent':
                c = Trainee_attendence(trainee_id=pk,attendence=False,date=g)
                c.save()
                error = 'no'
                us = Trainer.objects.get(customuser_id=request.user.id)
                a = Trainee.objects.filter(trainer_id=us.id)
                t_date = datetime.today().strftime('%Y-%m-%d')
                return render(request,'trainer_markattendence.html',{'error':error,'aten':a,'t':t_date})
            
            else:
                return redirect('trainer_markattendence')

@login_required(login_url='loginpage')
def trainer_class_schedule(request):
    return render(request,'trainer_class_schedule.html')

@login_required(login_url='loginpage')
def trainer_class_action(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        date = request.POST['date']
        link = request.POST['linkk']
        trainer = Trainer.objects.get(customuser_id=request.user.id)
        c = Class_schedule(topic=topic,date=date,link=link,trainer_id=trainer.id)
        c.save()
        return redirect('trainer_class_schedule')

@login_required(login_url='loginpage')
def trainer_inbox(request):
    u = Trainer.objects.get(customuser_id=request.user.id)
    d = TrainerNotification.objects.filter(department_id=u.department_id)
    dd = TrainerNotification.objects.filter(forr_id = u.id)
    count = TrainerNotification.objects.filter(forr_id = u.id,is_read=False).count()
    return render(request,'trainer_inbox.html',{'d':d,'dd':dd,'count':count})


@login_required(login_url='loginpage')
def trainer_view_project(request):
    t = Trainer.objects.get(customuser_id=request.user.id)
    p = Trainee.objects.filter(trainer_id=t.id)
    return render(request,'trainer_view_project.html',{'p':p})

@login_required(login_url='loginpage')
def trainer_viewaction_project(request,pk):
    d = SubmitedProject.objects.filter(trainee_id=pk)
    p = Trainee.objects.get(id=pk)
    return render(request,'trainer_viewaction_project.html',{'d':d,'p':p})

@login_required(login_url='loginpage')
def trainer_view_self_attendence(request):
    return render(request,'trainer_view_self_attendence.html')

@login_required(login_url='loginpage')
def trainer_view_self_attendence_action(request):
    
    if request.method == 'POST':
        user = request.user.id
        c = Trainer.objects.get(customuser_id=user)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        s = Trainer_attendence.objects.filter(trainer_id=c.id,date__range=(a,b)).order_by(sort_param)
        return render(request,'trainer_see_self_attendence.html',{'s':s,'a':a,'b':b})

@login_required(login_url='loginpage')
def trainer_trainee_attendence(request):
    return render(request,'trainer_trainee_attendence.html')

@login_required(login_url='loginpage')
def trainer_view_trainee_attendence(request):
    user = Trainer.objects.get(customuser_id=request.user.id)
    tr = Trainee.objects.filter(trainer_id=user)
    return render(request,'trainer_view_trainee_attendence.html',{'tr':tr})

@login_required(login_url='loginpage')
def trainer_view_trainee_attendence_action(request):
    if request.method == 'POST':
        trai = request.POST['traine']
        gg = Trainee.objects.get(id=trai)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        s = Trainee_attendence.objects.filter(trainee_id=trai,date__range=(a,b)).order_by(sort_param)
        return render(request,'trainer_see_trainee_attendence.html',{'s':s,'gg':gg,'a':a,'b':b})
    
@login_required(login_url='loginpage')
def trainer_view_trainee_card(request,pk):
    card = Trainee.objects.get(id=pk)
    return render(request,'trainer_view_trainee_card.html',{'i':card})

@login_required(login_url='loginpage')
def trainer_editprofile(request):
    t = Trainer.objects.get(customuser_id=request.user.id)
    return render(request,'trainer_editprofile.html',{'t':t})

@login_required(login_url='loginpage')
def trainer_update(request,pk):
    t = Trainer.objects.get(id=pk)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        contact = request.POST['contact']
        age = request.POST['age']
        if len(request.FILES) != 0:
            image = request.FILES['image']
        else:
            image = t.image
        p = ProfileEdit(sender=t.customuser,message=f'{t.customuser.first_name} {t.customuser.last_name} with email "{t.customuser.email}" has made some changes to their profile',is_read=False,is_approved=None,is_edited=True,firstname=fname,lastname=lname,email=email,contact=contact,age=age,image=image,trainer_id=t.id)
        p.save()
        
        error = 'no'
        return render(request,'trainerdash.html',{'p':p,'error':error,'t':t})

@login_required(login_url='loginpage')
def trainer_markasread(request,pk):
    m = TrainerNotification.objects.get(id=pk)
    m.is_read = True
    m.save()
    return redirect('trainer_inbox')

@login_required(login_url='loginpage')
def trainer_sendmail(request):
    bb = Trainer.objects.get(customuser_id=request.user.id)
    st = Trainee.objects.filter(trainer_id=bb.id)
    if request.method == 'POST':
        msg = request.POST['message']
        for i in st:
            dd = TraineeNotification(message=msg,forr_id=i.id,is_read=False,sender_id=bb.id)
            dd.save()
        error = 'no'
        return  HttpResponse(str({'error':error}))

    
# -----------------------------------teacher end------------------------------
