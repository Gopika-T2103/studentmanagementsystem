from django.urls import path
from . views import front_view,login_view,principal_dashboard,teacher_dashboard,student_dashboard,signup,add_teacher,all_teachers,update_teacher,delete_teacher
urlpatterns=[
    path('',front_view,name='front'),
    path('login/',login_view,name='login'),
    path('signup/', signup, name='signup'),
    path('principal/dashboard',principal_dashboard,name='principal_dashboard'),
    path('teacher/dashboard',teacher_dashboard,name='teacher_dashboard'),
    path('student/dashboard',student_dashboard,name='student_dashboard'),
    path('add_teacher/',add_teacher,name='add_teacher'),
    path('all_teachers/',all_teachers,name='all_teachers'),
    path('update_teacher/<int:id>/',update_teacher,name='update_teacher'),
    path('delete_teacher/<int:id>/',delete_teacher,name='delete_teacher'),
]