from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('admin',views.admin,name='admin'),
    path('signup',views.signup,name='signup'),
    path('signupaction',views.signupaction,name='signupaction'),
    path('loginaction',views.loginaction,name='loginaction'),
    path('course',views.course,name='course'),
    path('addcourse',views.addcourse,name='addcourse'),
    path('traineerecord',views.traineerecord,name='traineerecord'),
    path('trainerrecord',views.trainerrecord,name='trainerrecord'),
    path('approve',views.approve,name='approve'),
    path('approveaction/<int:pk>',views.approveaction,name='approveaction'),
    path('dept',views.dept,name='dept'),
    path('depadd',views.depadd,name="depadd"),
    path('notification',views.notification,name='notification'),
    path('traineecard/<int:pk>',views.traineecard,name='traineecard'),
    path('trainercard/<int:pk>',views.trainercard,name='trainercard'),
    path('newreg/<int:pk>',views.newreg,name='newreg'),
    path('records',views.records,name='records'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('assign',views.assign,name='assign'),
    path('assignaction/<int:pk>',views.assignaction,name='assignaction'),
    path('traineehome',views.traineehome,name='traineehome'),
    path('trainerhome',views.trainerhome,name='trainerhome'),
    path('managetrainee',views.managetrainee,name='managetrainee'),
    path('trainernoti/<int:pk>',views.trainernoti,name='trainernoti'),
    path('trainerdash',views.trainerdash,name='trainerdash'),
    # path('qw',views.qw,name='qw')
    
    
    


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)