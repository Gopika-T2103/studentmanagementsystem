
from django.shortcuts import render,redirect,get_object_or_404
from .models import customuser
from .models import Teacher
from django.contrib import messages
from .models import Student,Attendance,Marks
from django.contrib.auth import authenticate,login

# Create your views here.
def login_view(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        role=request.POST.get('role')
        try:
            user = customuser.objects.get(email=email, password=password, role=role)
        except customuser.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid email or password',
                'show':'login'
            })

        # Store user in session manually
        request.session['email'] = user.email
        request.session['role'] = user.role

        # if user is not None:
        #     login(request,user)

        if user.role=='principal':
                return redirect('principal_dashboard')
        elif user.role=='teacher':
                return redirect('teacher_dashboard')
        elif user.role=='student':
                return redirect('student_dashboard')
        # else:
        #     return render(request,'login.html',{'error':'Invalid username or password'})
        
    return render(request,'login.html',{
         'show': 'login'
    })

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        role=request.POST.get("role")

        if password!=confirmpassword:
            return render(request,'login.html',{
                "alert":"Passwords are not match",
                "show":"signup"
            })
        
        if customuser.objects.filter(email=email).exists():
            return render(request,"login.html",{
                "alert":"Email Already registered",
                "show":"signup"
            })
        
        user=customuser(
            username=username,
            email=email,
            password=password,
            role=role
        )
        
        user.save()

        return render(request, 'login.html', {
            "alert": "Signup successful! Please login",
            "show": "login"
        })
    return render(request,'login.html',{
        "show":"signup"
        })

def principal_dashboard(request):
    return render(request,'principal_dashboard.html')

def teacher_dashboard(request):
    return render(request,'teacher_dashboard.html')

def student_dashboard(request):
    return render(request,'student_dashboard.html')

def front_view(request):
     return render(request,'Front.html')


def add_teacher(request):
    if request.method=='POST':
        tname=request.POST.get("tname")
        teacher_id=request.POST.get("teacher_id")
        temail=request.POST.get("temail")
        tdept=request.POST.get("tdept")
        tassign=request.POST.get("tassign")


        Teacher.objects.create(
            tname=tname,
            teacher_id=teacher_id,
            temail=temail,
            tdept=tdept,
            tassign=tassign
        )
        messages.success(request,"New Teacher Added succesfully")
        return redirect("all_teachers")
    return render(request,"add_teacher.html",)

def all_teachers(request):
    teachers=Teacher.objects.all()
    return render(request,"all_teachers.html",{"teachers":teachers})


def update_teacher(request,id):
    teacher=Teacher.objects.get(id=id)
    if request.method=='POST':
         teacher.tname=request.POST.get('tname')
         teacher.temail=request.POST.get('temail')
         teacher.tdept=request.POST.get('tdept')
         teacher.tassign=request.POST.get('tassign')
         teacher.save()

         messages.success(request,"Teacher details Updated Succesfully!")
         return redirect("all_teachers")
    return redirect("all_teachers")

def delete_teacher(request,id):
    teacher=Teacher.objects.get(id=id)
    teacher.delete()
    messages.success(request,"Teacher data delete Succesfully!")

    return redirect("all_teachers")



def all_students(request):
    students = Student.objects.all()
    return render(request, "principal/all_students.html", {"students": students})


def student_attendance(request, id):
    Student = get_object_or_404(Student, id=id)
    Attendance = Attendance.objects.filter(Student=Student)
    return render(request, "principal/student_attendance.html", {
        "student": Student,
        "attendance": Attendance
    })


def student_marks(request, id):
    Student = get_object_or_404(Student, id=id)
    Marks = Marks.objects.filter(Student=Student)
    return render(request, "principal/student_marks.html", {
        "student": Student,
        "marks": Marks
    })
