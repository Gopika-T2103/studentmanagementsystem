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
    tassign=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.tname