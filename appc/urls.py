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
    path('trainee_dash',views.trainee_dash,name='trainee_dash'),
    path('trainerhome',views.trainerhome,name='trainerhome'),
    path('managetrainee',views.managetrainee,name='managetrainee'),
    path('traineenoti/<int:pk>',views.traineenoti,name='traineenoti'),
    path('trainerdash',views.trainerdash,name='trainerdash'),
    path('trainerleave',views.trainerleave,name='trainerleave'),
    path('trainer_assignproject',views.trainer_assignproject,name='trainer_assignproject'),
    path('trainer_assignproject_action',views.trainer_assignproject_action,name='trainer_assignproject_action'),
    path('trainerleaveapply',views.trainerleaveapply,name='trainerleaveapply'),
    path('applyleaveaction',views.applyleaveaction,name='applyleaveaction'),
    path('trainer_seeleave',views.trainer_seeleave,name='trainer_seeleave'),
    path('logoutt',views.logoutt,name="logoutt"),
    path('trainer_markattendence',views.trainer_markattendence,name="trainer_markattendence"),
    path('trainer_markaction/<int:pk>',views.trainer_markaction,name='trainer_markaction'),
    path('trainer_class_schedule',views.trainer_class_schedule,name='trainer_class_schedule'),
    path('trainer_class_action',views.trainer_class_action,name='trainer_class_action'),
    path('trainee_inbox',views.trainee_inbox,name='trainee_inbox'),
    path('trainee_project',views.trainee_project,name='trainee_project'),
    path('trainee_class',views.trainee_class,name='trainee_class'),
    path('trainee_attendence',views.trainee_attendence,name='trainee_attendence'),
    path('trainee_applyleave',views.trainee_applyleave,name='trainee_applyleave'),
    path('assignedtask',views.assignedtask,name='assignedtask'),
    path('submittask/<int:pk>',views.submittask,name='submittask'),
    path('submittaskaction/<int:pk>',views.submittaskaction,name='submittaskaction'),
    path('completedtask',views.completedtask,name='completedtask'),
    path('trainee_viewattendence',views.trainee_viewattendence,name='trainee_viewattendence'),
    path('admin_mark_trainerattendence',views.admin_mark_trainerattendence,name="admin_mark_trainerattendence"),
    path('admin_mark_trainerattendence_action/<int:pk>',views.admin_mark_trainerattendence_action,name="admin_mark_trainerattendence_action"),
    path('trainer_attendence',views.trainer_attendence,name="trainer_attendence"),
    path('admin_view_trainerattendence',views.admin_view_trainerattendence,name="admin_view_trainerattendence"),
    path('admin_view_trainerattendence_action',views.admin_view_trainerattendence_action,name="admin_view_trainerattendence_action"),
    path('admin_show_trainerattendence',views.admin_show_trainerattendence,name="admin_show_trainerattendence"),
    path('admin_view_trainee_attendence',views.admin_view_trainee_attendence,name="admin_view_trainee_attendence"),
    path('admin_view_trainee_attendence_action',views.admin_view_trainee_attendence_action,name="admin_view_trainee_attendence_action"),
    path('admin_sendmail',views.admin_sendmail,name="admin_sendmail"),
    path('disapproveaction/<int:pk>',views.disapproveaction,name='disapproveaction'),
    # path('qw',views.qw,name='qw'),
    
    
    


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)