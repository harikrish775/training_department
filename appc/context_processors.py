from appc.models import Notification,ProfileEdit,Trainer,TrainerNotification,Trainee,TraineeNotification,Class_schedule
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

def notifications(request):
    # Calculate the notification count
    
    co = Notification.objects.filter(is_read=False).count()
    po = ProfileEdit.objects.filter(is_approved='').count()
    ko = co+po
    noti = Notification.objects.filter(is_read = False)
    pp = ProfileEdit.objects.filter(is_approved='')
    
    return {'ko': ko,'noti':noti,'pp':pp}



def trainernoti(request):
    if not request.user.is_authenticated:
        return {'count': 0}  # Default value if user is not authenticated

    if request.user.is_special and not request.user.is_superuser:
        try:
            u = Trainer.objects.get(customuser_id=request.user.id)
            count = TrainerNotification.objects.filter(forr_id=u.id, is_read=False).count()
            return {'count': count}
        except Trainer.DoesNotExist:
            pass  # Handle the case where Trainer object does not exist for the user
    
    return {'count': 0}

def traineenoti(request):
    if not request.user.is_authenticated:
        return {'count': 0}  # Default value if user is not authenticated
    
    if not request.user.is_special and not request.user.is_superuser :
        try:
            today = date.today()
            fg =Trainee.objects.get(customuser_id=request.user.id)
            n = TraineeNotification.objects.filter(is_read=False,forr_id = fg.id).count()
            co = Class_schedule.objects.filter(date=today,trainer_id=fg.trainer_id).count()
            dd = TraineeNotification.objects.filter(forr_id = fg.id)
           
            return {'count': n,'co':co,'dd':dd}
        except Trainer.DoesNotExist:
            pass  # Handle the case where Trainer object does not exist for the user

    return {'count': 0}
    
        
        
    

