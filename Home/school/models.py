from django.db import models
# from django.contrib.auth.models import AbstractUser

# Create your models here.

class customuser(models.Model):
    username=models.CharField(max_length=255,blank=True,null=True)
    email=models.CharField(max_length=255,unique=True,primary_key=True)
    password=models.CharField(max_length=255)
    ROLE_CHOICES=(
        ('principal','Principal'),
        ('teacher','Teacher'),
        ('student','Student'),
    )
    
    role=models.CharField(max_length=255,choices=ROLE_CHOICES)
    
    # def __str__(self):
    #     return self.email



class Teacher(models.Model):
    tname=models.CharField(max_length=255)
    teacher_id=models.CharField(max_length=255,unique=True)
    temail=models.CharField(max_length=255)
    tdept=models.CharField(max_length=255)
    tassign=models.CharField(max_length=255)

    def __str__(self):
        return self.tname
    

# class classteacher(models.Model):
#     name=models.CharField(max_length=255)
#     email=models.CharField(max_length=255,unique=True)

#     def __str__(self):
#         return self.name
    

class Student(models.Model):
    name=models.CharField(max_length=255)
    roll_no=models.IntegerField(max_length=255)
    class_name = models.CharField(max_length=50)
    # class_teacher = models.ForeignKey(classteacher, on_delete=models.SET_NULL, null=True)

    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    guardian_address = models.TextField()

    def __str__(self):
        return self.name
    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)   # Present / Absent


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks = models.IntegerField()