
from django.shortcuts import render,redirect,get_object_or_404
from .models import customuser
from .models import Teacher
from django.contrib import messages
from .models import Student,Attendance,Marks
from django.contrib.auth import authenticate,login
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import date
import datetime

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
   
    # ensure user is teacher
    if request.session.get('role') !='teacher':
         return redirect('login')
    
    teacher_email=request.session.get('email')

    # get teacher record
    teacher=Teacher.objects.get(temail=teacher_email)

    assigned_class=teacher.tassign

    # get all students in the class
    students=Student.objects.filter(class_name=assigned_class)

    today = date.today()

    morning_present = Attendance.objects.filter(
        student__class_name=assigned_class,
        date=today,
        session="morning",
        status="Present"
    ).count()

    afternoon_present = Attendance.objects.filter(
        student__class_name=assigned_class,
        date=today,
        session="afternoon",
        status="Present"
    ).count()

    total_present = morning_present + afternoon_present
    total_absent = (len(students) * 2) - total_present

    # load all marks for those students
    marks=Marks.objects.filter(student__in=students)

    # subject details
    subjects=['Mathematics','Biology','Physics','Chemistry','Malayalam','English','Hindi']

    result_counts=[]
    for sub in subjects:
        passed=marks.filter(subject=sub,marks__gte=20).count()  #pass=marks>=20
        result_counts.append(passed)

    return render(request,'teacher_dashboard.html', {
        "teacher":teacher,
        'assigned_class':assigned_class,
        'subjects':subjects,
        "result_counts":result_counts,

        "morning_present": morning_present,
        "afternoon_present": afternoon_present,
        "total_present": total_present,
        "total_absent": total_absent,
    })


    


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


def update_teacher(request, id):
    teacher = Teacher.objects.get(id=id)

    if request.method == 'POST':
        teacher.tname = request.POST.get('tname')
        teacher.temail = request.POST.get('temail')
        teacher.tdept = request.POST.get('tdept')
        teacher.tassign = request.POST.get('tassign')
        teacher.save()

        messages.success(request, "Teacher details updated successfully!")
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


def class_list_view(request):
    # only teacher can access
    if request.session.get('role') !='teacher':
         return redirect('login')
    teacher_email=request.session.get('email')
    teacher=Teacher.objects.get(temail=teacher_email)
    assigned_class=teacher.tassign

    # load only assigned class students
    students=Student.objects.filter(class_name=assigned_class)\
        .annotate(
             roll_int=Cast("roll_no",IntegerField())
        ).order_by("roll_int")

    return render(request,'teacher_class_list.html',{
         "students":students,
         "assigned_class":assigned_class
    })



def add_student(request):
     if request.session.get('role')!='teacher':
          return redirect('login')
     teacher_email=request.session.get('email')
     teacher=Teacher.objects.get(temail=teacher_email)
     assigned_class=teacher.tassign

     if request.method=='POST':
          name=request.POST.get('name')
          roll_no=request.POST.get("roll_no")

          admission_number = request.POST.get('admission_number')
          admission_date = request.POST.get('admission_date')
          date_of_birth = request.POST.get('date_of_birth')
          gender = request.POST.get('gender')

          guardian_name=request.POST.get("guardian_name")
          guardian_phone=request.POST.get("guardian_phone")
          guardian_address=request.POST.get("guardian_address")

          Student.objects.create(
               name=name,
               roll_no=roll_no,
               class_name=assigned_class,

               admission_number=admission_number,
               admission_date=admission_date,
               date_of_birth=date_of_birth,
               gender=gender,
               status="Active",

               guardian_name=guardian_name,
               guardian_phone=guardian_phone,
               guardian_address=guardian_address
          )

          messages.success(request,"New Student added succesfully!!!")
          return redirect("class_list")
     
     return render(request,"add_student.html",{
          "assigned_class":assigned_class
     })



def add_marks(request):
    # Only teacher can access
    if request.session.get('role') != 'teacher':
        return redirect('login')

    teacher_email = request.session.get('email')
    teacher = Teacher.objects.get(temail=teacher_email)
    assigned_class = teacher.tassign

    # Load all students in this class
    students = Student.objects.filter(class_name=assigned_class).annotate(
        roll_int=Cast("roll_no", IntegerField())
    ).order_by("roll_int")

    # Subjects taught in the school
    subjects = ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'Malayalam', 'English', 'Hindi']

    if request.method == "POST":
        student_id = request.POST.get("student")
        subject = request.POST.get("subject")
        marks = request.POST.get("marks")

        student_obj=Student.objects.get(id=student_id)

        Marks.objects.create(
            student=student_obj,
            subject=subject,
            marks=marks,
            student_name=student_obj.name,
            class_name=student_obj.class_name,
        )

        messages.success(request, "Marks Added Successfully!")
        return redirect("add_marks")

    return render(request, "add_marks.html", {
        "students": students,
        "subjects": subjects,
        "assigned_class": assigned_class
    })



def view_marks(request):
    # Only teacher can access
    if request.session.get('role') != 'teacher':
        return redirect('login')

    teacher_email = request.session.get('email')
    teacher = Teacher.objects.get(temail=teacher_email)
    assigned_class = teacher.tassign

    # load students of that class
    students = Student.objects.filter(class_name=assigned_class).annotate(
        roll_int=Cast("roll_no", IntegerField())
    ).order_by("roll_int")

    # Subjects in school
    subjects = ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'Malayalam', 'English', 'Hindi']

    # Save marks on POST
    if request.method == "POST":
        student_id = request.POST.get("student")
        subject = request.POST.get("subject")
        marks = request.POST.get("marks")

        Marks.objects.create(student_id=student_id,subject=subject,marks=marks)

        messages.success(request,"Marks Added Succesfullly!!!")
        return redirect("view_marks")
        # GROUP MARKS BY STUDENT
    marks_list = {}
    for stu in students:
        marks_list[stu.id] = {
            'student': stu,
            'marks': {sub: "-" for sub in subjects}
        }

    all_marks = Marks.objects.filter(student__in=students)

    for m in all_marks:
        if m.subject in subjects:
            marks_list[m.student.id]['marks'][m.subject] = m.marks

    return render(request, "view_marks.html", {
        "students": students,
        "subjects": subjects,
        "assigned_class": assigned_class,
        "marks_list": marks_list
    })


# edit Marks

def update_marks(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        subjects = ['Mathematics','Biology','Physics','Chemistry','Malayalam','English','Hindi']

        student = Student.objects.get(id=student_id)

        for sub in subjects:
            new_marks = request.POST.get(sub)

            if new_marks and new_marks != "-":
                Marks.objects.update_or_create(
                    student=student,
                    subject=sub,
                    defaults={'marks': new_marks}
                )

        return redirect("view_marks")
    

def select_attendance_session(request):
    if request.session.get('role') !='teacher':
        return redirect('login')
    
    return render(request,'attendance_select_session.html')


def mark_attendance(request, session):
    if request.session.get('role') != 'teacher':
        return redirect('login')

    # Block weekends
    if datetime.date.today().weekday() > 4:
        return render(request, "error.html", {"message": "Attendance allowed only Monday–Friday"})

    teacher_email = request.session.get('email')
    teacher = Teacher.objects.get(temail=teacher_email)
    assigned_class = teacher.tassign

    students = Student.objects.filter(class_name=assigned_class).order_by("roll_no")
    today = date.today()

    if request.method == "POST":
        for stu in students:
            status = request.POST.get(f"status_{stu.id}")

            Attendance.objects.update_or_create(
                student=stu,
                date=today,
                session=session,
                defaults={
                    "status": status,
                    "student_name": stu.name,
                    "student_class": stu.class_name,
                }
            )

        messages.success(request, f"{session.capitalize()} attendance saved!")
        return redirect("mark_attendance", session=session)

    # Count attendance for summary
    morning_present = Attendance.objects.filter(
        student__class_name=assigned_class,
        date=today,
        session="morning",
        status="Present"
    ).count()

    afternoon_present = Attendance.objects.filter(
        student__class_name=assigned_class,
        date=today,
        session="afternoon",
        status="Present"
    ).count()

    total_present = morning_present + afternoon_present
    total_absent = (len(students) * 2) - total_present

    return render(request, "attendance_mark.html", {
        "students": students,
        "session": session,
        "today": today,
        "assigned_class": assigned_class,
        "morning_present": morning_present,
        "afternoon_present": afternoon_present,
        "total_present": total_present,
        "total_absent": total_absent,
    })



def edit_attendance(request):
    if request.session.get('role') != 'teacher':
        return redirect('login')

    teacher_email = request.session.get('email')
    teacher = Teacher.objects.get(temail=teacher_email)
    assigned_class = teacher.tassign

    today = date.today()

    records = Attendance.objects.filter(
        student__class_name=assigned_class,
        date=today
    ).order_by("student__roll_no")

    if request.method == "POST":
        for row in records:
            new_status = request.POST.get(f"status_{row.id}")
            row.status = new_status
            row.save()

        messages.success(request, "Attendance updated successfully!")
        return redirect("edit_attendance")

    return render(request, "attendance_edit.html", {
        "records": records,
        "today": today,
    })



# edit the student details in the teacher dashboard

def edit_student(request,id):
    student=get_object_or_404(Student,id=id)
    if request.method=='POST':
        student.name=request.POST.get('name')
        student.roll_no=request.POST.get("roll_no")

        student.admission_number=request.POST.get('admission_number')
        student.admission_date=request.POST.get('admission_date')
        student.date_of_birth=request.POST.get('date_of_birth')
        student.gender=request.POST.get('gender')

        student.status = request.POST.get('status')
        student.passed_out_year = request.POST.get('passed_out_year')
        student.tc_issued_date = request.POST.get('tc_issued_date')

        student.guardian_name=request.POST.get("guardian_name")
        student.guardian_phone=request.POST.get("guardian_phone")
        student.guardian_address=request.POST.get("guardian_address")
        print("Passed Out Year Received =", request.POST.get('passed_out_year'))
        student.save()

        messages.success(request,"Student details updated successfully!!")
        return redirect('class_list')
    return redirect("class_list")