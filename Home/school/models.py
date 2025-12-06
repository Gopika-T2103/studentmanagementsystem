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




class Teacher(models.Model):
    STATUS_CHOICES=(
        ("Active","Active"),
        ("Resigned","Resigned"),
        ("Retired","REtired")
    )
    tname=models.CharField(max_length=255)
    teacher_id=models.CharField(max_length=255,unique=True)
    temail=models.CharField(max_length=255)
    tdept=models.CharField(max_length=255)
    tassign=models.CharField(max_length=255,null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="Active")
    # user = models.OneToOneField(customuser, on_delete=models.CASCADE)
    # subject = models.CharField(max_length=50) 

    def __str__(self):
        return self.tname
    

# class classteacher(models.Model):
#     name=models.CharField(max_length=255)
#     email=models.CharField(max_length=255,unique=True)

#     def __str__(self):
#         return self.name
    

class Student(models.Model):
    name=models.CharField(max_length=255)
    roll_no=models.IntegerField()
    class_name = models.CharField(max_length=50)
    # class_teacher = models.ForeignKey(classteacher, on_delete=models.SET_NULL, null=True)

    admission_number=models.CharField(max_length=50,null=True,blank=True)
    admission_date=models.DateField(null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)

    gender=models.CharField(
        max_length=10,
        choices=(('Male',"Male"),("Female","Female"),("Other","Other")),
        null=True,blank=True
    )

    status=models.CharField(
        max_length=20,
        choices=(
            ("Active","Active"),
            ("Inactive","Inactive"),
            ("Passed Out","Passed Out"),
            ("TC Issued","TC Issued")
        ),
        default="Active"
    )

    passed_out_year=models.CharField(max_length=10,null=True,blank=True)
    tc_issued_date=models.DateField(null=True,blank=True)


    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    guardian_address = models.TextField()

    def __str__(self):
        return self.name
    

    # Attendance Percentage Function
    def attendance_percentage(self):
        from .models import Attendance   # avoid circular import

        records = Attendance.objects.filter(student=self)

        if not records:
            return 0   # no attendance → 0%

        # Each Present = 1 point (morning or afternoon)
        earned = sum(1 for r in records if r.status == "Present")
        total = len(records)  # total sessions

        return round((earned / total) * 100, 2)


class Attendance(models.Model):
    SESSION_CHOICES=(
        ('morning','Morning'),
        ('afternoon','Afternoon'),
    )

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_name=models.CharField(max_length=255,default='Unknown')
    student_class=models.CharField(max_length=20,default='Unknown')

    date = models.DateField()
    session=models.CharField(max_length=20,choices=SESSION_CHOICES,default='morning')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)   # Present / Absent

    class Meta:
        unique_together=('student','date','session')

    def __str__(self):
        return f"{self.student_name} - {self.date} ({self.session})"
    

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks = models.IntegerField()
    student_name=models.CharField(max_length=255,null=True,blank=True)
    class_name=models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        unique_together=('student','subject')


