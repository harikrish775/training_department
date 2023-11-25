from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from .models import Trainee,Trainer,Course,Notification,CustomUser,Department,TrainerNotification,TraineeNotification,Project,TrainerLeave,Trainee_attendence,Class_schedule,Trainer_attendence,TempSignup,SubmitedProject,TraineeNotificationStatus,TrainerNotificationStatus,TraineeLeave
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
import random,string
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime,date

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
        course = request.POST['course']
        image = request.FILES['image']
        rr = request.POST['rrr']
        department = request.POST['department'] 
        degree = request.FILES['degree']
        # propass = generate_password()
        propass = '123'

        if rr == 'trainee':
                te = TempSignup(first_name=firstname,last_name=lastname,username=username,email=email,password=propass,contact=contact,joindate=joindate,age=age,gender=gender,course_id=course,image=image,department_id=department,degree=degree)
                te.save()
                no = Notification(message=f' A new {rr} registered as {firstname} {lastname} is waiting for your approval.',tempsignup_id=te.id )
                no.save()
                return redirect('loginpage')
            
        elif rr == 'trainer':
                te = TempSignup(first_name=firstname,last_name=lastname,username=username,email=email,password=propass,contact=contact,joindate=joindate,age=age,gender=gender,course_id=course,image=image,department_id=department,degree=degree,is_special=True)
                te.save()
                no = Notification.objects.create(message=f'A new {rr} has registered as {firstname} {lastname}.',tempsignup_id=te.id )
                no.save()
                return redirect('loginpage')
        
# -------------------------------------student----------------
def trainee_dash(request):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    return render(request,'trainee_dash.html',{'count':n,'co':co})

def trainee_inbox(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    j = TraineeNotification.objects.all()
    n = TraineeNotification.objects.filter(is_read=False).count()
    return render(request,'trainee_inbox.html',{'no':j,'count':n,'co':co})

def trainee_project(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    
    return render(request,'trainee_project.html',{'count':n,'co':co})

def assignedtask(request):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()

    sp = SubmitedProject.objects.filter(trainer_id=fg.trainer)
    p = Project.objects.filter(trainer_id=fg.trainer)
    return render(request,'assignedtask.html',{'v':p,'sp':sp,'co':co,'count':n})

def submittask(request,pk):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()

    m = Project.objects.get(id=pk)
    return render(request,'submittask.html',{'m':m,'co':co,'count':n})

def submittaskaction(request,pk):
    g = Project.objects.get(id=pk)
    if request.method == 'POST':
        trainee = Trainee.objects.get(customuser_id=request.user.id)
        description = request.POST['des']
        file = request.FILES['docc']
        status = True
        today = date.today()
       
        if today > g.enddate:
            h = SubmitedProject(projectname=g.projectname,startdate=g.startdate,enddate=g.enddate,description=description,status=status,file=file,trainee_id=trainee.id,trainer_id=g.trainer_id,is_delay=True)
            h.save()
            return redirect('trainee_dash')
        else:
            h = SubmitedProject(projectname=g.projectname,startdate=g.startdate,enddate=g.enddate,description=description,status=status,file=file,trainer_id=g.trainer_id,trainee_id=trainee.id)
            h.save()
            return redirect('trainee_dash')
        
    
def completedtask(request):
    n = TraineeNotification.objects.filter(is_read=False).count()
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    h = Project.objects.filter(status=True)
    return render(request,'completedtask.html',{'h':h,'co':co,'count':n})



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

def trainee_attendence(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    return render(request,'trainee_attendence.html',{'count':n,'co':co})

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



def trainee_applyleave(request):
    today = date.today()
    fg =Trainee.objects.get(customuser_id=request.user.id)
    co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
    n = TraineeNotification.objects.filter(is_read=False).count()
    return render(request,'trainee_applyleave.html',{'count':n,'co':co})

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


# --------------------------------------student end-------------------------
            

# -------------------------------admin---------------------

def notification(request):
    co = Notification.objects.filter(is_read=False).count()
    no1 = Notification.objects.filter(is_read=False)
    no = Notification.objects.all()
    return render(request,'notification.html',{'no':no,'ncount':co,'noti':no1})

def admin_sendmail(request):
    if request.method == 'POST':
        todeptrainers = request.POST['todeptrainers']
        if todeptrainers == 'all':
            mess = request.POST['message']
            h = TrainerNotification(message=mess)
            h.save()
            return redirect('dashboard')
        else:
            mess = request.POST['message']
            h = TrainerNotification(message=mess,department_id=todeptrainers)
            h.save()
            return redirect('dashboard')
    

def records(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'records.html',{'ncount':co,'noti':no})

def dashboard(request):
    b = TrainerLeave.objects.filter(is_read=False).count()
    c = TraineeLeave.objects.filter(is_read=False).count()
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    e = Trainee.objects.all().count()
    r = Trainer.objects.all().count()
    dep = Department.objects.all()
    return render(request,'dashboard.html',{'dep':dep,'ecount':e,'rcount':r,'ncount':co,'noti':no,'b':b,'c':c})

def assign(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    teach = Trainer.objects.all()
    asign = Trainee.objects.all()
    return render(request,'assign.html',{'asign':asign,'teach':teach,'ncount':co,'noti':no})

def assignaction(request,pk):
    teach = Trainer.objects.all()
    asign = Trainee.objects.all()
    if request.method == 'POST':
        co = Notification.objects.filter(is_read=False).count()
        no = Notification.objects.filter(is_read=False)
        t = request.POST['trainr']
        c = Trainee.objects.get(id=pk)
        c.trainer_id = t
        c.save()
        return render(request,'assign.html',{'asign':asign,'teach':teach,'ncount':co,'noti':no})
    
def course(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'course.html',{'ncount':co,'noti':no})

def traineerecord(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    rec = Trainee.objects.all()
    return render(request,'trainee_record.html',{'rec':rec,'ncount':co,'noti':no})

def trainerrecord(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    rece = Trainer.objects.all()
    return render(request,'trainer_record.html',{'rece':rece,'ncount':co,'noti':no})

def traineecard(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    card = Trainee.objects.get(id=pk)
    return render(request,'trainee_card.html',{'i':card,'ncount':co,'noti':no})

def trainercard(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    card = Trainer.objects.get(id=pk)
    return render(request,'trainer_card.html',{'i':card,'ncount':co,'noti':no})

def approve(request):
    global co,no
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    te = Notification.objects.all()
    return render(request,'aprove.html',{'te':te,'ncount':co,'noti':no})

def newreg(request,pk):
    b = Notification.objects.get(id=pk)
    return render(request,'new_reg.html',{'i':b,'ncount':co,'noti':no})

def approveaction(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    n = Notification.objects.get(id=pk)
    n.is_read = True
    n.is_approved = True
    n.save()
    
    if n.tempsignup.is_special :
        trainer = TempSignup.objects.get(id=n.tempsignup_id)
        userr = CustomUser.objects.create_user(first_name=trainer.first_name,last_name=trainer.last_name,email=trainer.email,username=trainer.username,password=trainer.password,is_special=trainer.is_special,date_joined=trainer.joindate)
        userr.save()
        approved_trainer = Trainer(contact=trainer.contact,age=trainer.age,gender=trainer.gender,joindate=trainer.joindate,course_id=trainer.course_id,image=trainer.image,customuser=userr,department_id=trainer.department_id,degree=trainer.degree)
        approved_trainer.save()
        n.trainer_id = approved_trainer
        n.sender = userr
        n.save()

        subject = 'Your approval has been successful'
        message = f'Hy {n.sender.first_name} {n.sender.last_name}, \n Congratulations on being a part of ALTOS family. \n Your Login Credentials : \n Username: {n.sender.email} \n Password: {trainer.password} '
        recipient = n.sender.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        messages.info(request,f'{n.sender.first_name}{n.sender.last_name} has been approved')
        return redirect('approve')
        
    
    else:
        trainee = TempSignup.objects.get(id=n.tempsignup_id)
        userr = CustomUser.objects.create_user(first_name=trainee.first_name,last_name=trainee.last_name,email=trainee.email,username=trainee.username,password=trainee.password,is_special=trainee.is_special,date_joined=trainee.joindate)
        userr.save()
        approved_trainee = Trainee(contact=trainee.contact,age=trainee.age,gender=trainee.gender,joindate=trainee.joindate,course_id=trainee.course_id,image=trainee.image,customuser=userr,department_id=trainee.department_id,degree=trainee.degree)
        approved_trainee.save()
        n.trainee_id = approved_trainee
        n.sender = userr
        n.save()

        subject = 'Your approval has been successful'
        message = f'Hy {n.sender.first_name} {n.sender.last_name}, \n Congratulations on being a part of ALTOS family. \n Your Login Credentials : \n Username: {n.sender.email} \n Password: {trainee.password} '
        recipient = n.sender.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        messages.info(request,f'{n.sender.first_name}{n.sender.last_name} has been approved')
        return redirect('approve')
    
def disapproveaction(request,pk):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    n = Notification.objects.get(id=pk)
    n.is_read = True
    n.is_approved = False
    n.save()
    return redirect('approve')

def dept(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'department.html',{'ncount':co,'noti':no})

def depadd(request):
    if request.method == 'POST':
        dept = request.POST['dept']
        d = Department(departmentname=dept)
        d.save()
        error = 'no'
        return render(request,'department.html',{'error':error})

def addcourse(request):
    if request.method == 'POST':
        name = request.POST['course']
        fee = request.POST['fee']
        syllabus = request.POST['syl']
        co = Course(coursename=name,coursefee=fee,syllabus=syllabus)
        co.save()
        return redirect('course')
    
def trainer_attendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'trainer_attendence.html',{'ncount':co,'noti':no})

def admin_mark_trainerattendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    ho = Trainer.objects.all()
    t_date = datetime.today().strftime('%Y-%m-%d')
    return render(request,'admin_mark_trainerattendence.html',{'ho':ho,'t':t_date,'ncount':co,'noti':no})

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

def admin_view_trainerattendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    tr = Trainer.objects.all()
    return render(request,'admin_view_trainerattendence.html',{'tr':tr,'ncount':co,'noti':no})

def admin_view_trainerattendence_action(request):
    if request.method == 'POST':
        l = request.POST['trid']
        c = Trainer.objects.get(id=l)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        s = Trainer_attendence.objects.filter(trainer_id=c.id,date__range=(a,b)).order_by(sort_param)
        return render(request,'admin_show_trainerattendence.html',{'s':s,'c':c})
    
def admin_show_trainerattendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    return render(request,'admin_show_trainerattendence.html',{'ncount':co,'noti':no})

def admin_view_trainee_attendence(request):
    co = Notification.objects.filter(is_read=False).count()
    no = Notification.objects.filter(is_read=False)
    s = Trainee.objects.all()
    return render(request,'admin_view_trainee_attendence.html',{'s':s,'ncount':co,'noti':no})

def admin_view_trainee_attendence_action(request):
    if request.method == 'POST':
        l = request.POST['trrid']
        c = Trainee.objects.get(id=l)
        a = request.POST['start']
        b = request.POST['end']
        sort_param = request.GET.get('sort', 'date')
        ss = Trainee_attendence.objects.filter(trainee_id=c.id,date__range=(a,b)).order_by(sort_param)
        return render(request,'admin_show_trainee_attendence.html',{'ss':ss,'c':c,'ncount':co,'noti':no})
    
def admin_review_attendence(request):
    a = TrainerLeave.objects.all()
    b = TraineeLeave.objects.all()
    return render(request,'admin_review_attendence.html',{'leave':a,'bleave':b})

def admin_approve_leave(request,pk):
    a = TrainerLeave.objects.get(id=pk)
    a.is_approved = True
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')

def admin_reject_leave(request,pk):
    a = TrainerLeave.objects.get(id=pk)
    a.is_approved = False
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')

def admin_approve_leave_trainee(request,pk):
    a = TraineeLeave.objects.get(id=pk)
    a.is_approved = True
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')

def admin_reject_leave_trainee(request,pk):
    a = TraineeLeave.objects.get(id=pk)
    a.is_approved = False
    a.is_read = True
    a.save()
    return redirect('admin_review_attendence')
    

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
        return redirect('trainerdash') #-------------------------------------------------------------------------mail for trainee
    
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
        today = date.today()
        
        trainr = Trainer.objects.get(customuser_id=request.user.id)
        f = Project(projectname=name,startdate=startdate,enddate=enddate,dateassigned=today,trainer_id=trainr.id)
        f.save()
        return render(request,'trainer_assignproject.html')

def trainer_markattendence(request):
    us = Trainer.objects.get(customuser_id=request.user.id)
    a = Trainee.objects.filter(trainer_id=us.id)
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
        trainer = Trainer.objects.get(customuser_id=request.user.id)
        c = Class_schedule(topic=topic,date=date,link=link,trainer_id=trainer.id)
        c.save()
        return redirect('trainer_class_schedule')


def trainer_inbox(request):
    u = Trainer.objects.get(customuser_id=request.user.id)
    d = TrainerNotification.objects.filter(department_id=u.department_id)
    
    return render(request,'trainer_inbox.html',{'d':d})

# def trainer_readmessage(request,pk):
#     user = request.user.id
#     o = Trainer.objects.get(customuser_id=user)
#     a = TrainerNotification.objects.get(id=pk)
#     return render(request,'trainer_inbox.html')

def trainer_view_project(request):
    t = Trainer.objects.get(customuser_id=request.user.id)
    p = Trainee.objects.filter(trainer_id=t.id)
    return render(request,'trainer_view_project.html',{'p':p})

def trainer_viewaction_project(request,pk):
    d = SubmitedProject.objects.filter(trainee_id=pk)
    return render(request,'trainer_viewaction_project.html',{'d':d})

# -----------------------------------teacher end------------------------------
