from django.urls import path
from . views import front_view,login_view,principal_dashboard,teacher_dashboard,student_dashboard,signup,add_teacher,all_teachers,update_teacher,delete_teacher,all_students,student_attendance,student_marks,class_list_view
from .views import add_student,add_marks,view_marks
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
    path('all_students/',all_students,name='all_students'),
    path("student/<int:id>/attendance/",student_attendance, name="student_attendance"),
    path("student/<int:id>/marks/",student_marks, name="student_marks"),
    path("teacher/class_list/",class_list_view, name="class_list"),
    path("teacher/add_student",add_student,name="add_student"),
    path('teacher/add_marks/',add_marks,name='add_marks'),
    path("teacher/view_marks/", view_marks, name="view_marks"),

]