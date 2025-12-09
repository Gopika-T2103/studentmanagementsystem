
from django.shortcuts import render,redirect,get_object_or_404
from .models import customuser
from .models import Teacher
from django.contrib import messages
from .models import Student,Attendance,Marks
from django.contrib.auth import authenticate,login
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import date,timedelta,datetime
from django.utils import timezone
from django.urls import reverse

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


# UPDATE TEACHER FORM IN ALL TEACHER LIST
def update_teacher(request):
    if request.method == "POST":
        tid = request.POST.get("id")
        teacher = Teacher.objects.get(id=tid)

        teacher.tname = request.POST.get("tname")
        teacher.teacher_id = request.POST.get("teacher_id")
        teacher.temail = request.POST.get("temail")
        teacher.tdept = request.POST.get("tdept")
        teacher.tassign = request.POST.get("tassign")
        teacher.status = request.POST.get("status")

        teacher.save()
        messages.success(request, "Teacher details updated successfully!")
        return redirect("all_teachers")

# DELETE THE TEACHER FROM THE ALL TEACHER LIST
def resign_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    teacher.status = "Resigned"
    teacher.save()

    messages.success(request, "Teacher marked as resigned.")
    return redirect("all_teachers")




def all_students(request):

    # Get all class names sorted alphabetically
    classes=Student.objects.values_list('class_name',flat=True).distinct().order_by('class_name')
    classwise_students={}

    for cls in classes:

        # fetch students of that class
        students=Student.objects.filter(class_name=cls)\
        .annotate(roll_int=Cast("roll_no",IntegerField()))\
        .order_by("roll_no")   #sort by roll_bumber

        classwise_students[cls]=students
    return render(request,"all_students.html",{
        "classwise_students":classwise_students
    })

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
    

# def select_attendance_session(request):
#     if request.session.get('role') !='teacher':
#         return redirect('login')
    
#     return render(request,'attendance_select_session.html')


# def mark_attendance(request, session):
#     if request.session.get('role') != 'teacher':
#         return redirect('login')

    # Block weekends
    # if datetime.date.today().weekday() > 4:
    #     messages.error(request,  "Attendance allowed only Monday–Friday")
    #     return redirect("select_attendance_session")

    # teacher_email = request.session.get('email')
    # teacher = Teacher.objects.get(temail=teacher_email)
    # assigned_class = teacher.tassign

    # students = Student.objects.filter(class_name=assigned_class).order_by("roll_no")
    # today = date.today()

    # if request.method == "POST":
    #     for stu in students:
    #         status = request.POST.get(f"status_{stu.id}")

    #         Attendance.objects.update_or_create(
    #             student=stu,
    #             date=today,
    #             session=session,
    #             defaults={
    #                 "status": status,
    #                 "student_name": stu.name,
    #                 "student_class": stu.class_name,
    #             }
    #         )

    #     messages.success(request, f"{session.capitalize()} attendance saved!")
    #     return redirect("mark_attendance", session=session)

    # Count attendance for summary
#     morning_present = Attendance.objects.filter(
#         student__class_name=assigned_class,
#         date=today,
#         session="morning",
#         status="Present"
#     ).count()

#     afternoon_present = Attendance.objects.filter(
#         student__class_name=assigned_class,
#         date=today,
#         session="afternoon",
#         status="Present"
#     ).count()

#     total_present = morning_present + afternoon_present
#     total_absent = (len(students) * 2) - total_present

#     return render(request, "attendance_mark.html", {
#         "students": students,
#         "session": session,
#         "today": today,
#         "assigned_class": assigned_class,
#         "morning_present": morning_present,
#         "afternoon_present": afternoon_present,
#         "total_present": total_present,
#         "total_absent": total_absent,
#     })



# def edit_attendance(request):
#     if request.session.get('role') != 'teacher':
#         return redirect('login')

#     teacher_email = request.session.get('email')
#     teacher = Teacher.objects.get(temail=teacher_email)
#     assigned_class = teacher.tassign


#     #  GET DATE RANGE
#     today = date.today()

#       # default = current Monday → Friday
#     start_date=today - timedelta(days=today.weekday())
#     end_date=start_date +timedelta(days=4)

#     if request.GET.get("start") and request.GET.get("end"):
#         start_date=date.fromisoformat(request.GET.get("start"))
#         end_date=date.fromisoformat(request.GET.get("end"))


#     # LOAD CURRENT DAY RECORDS FOR EDITING
#     records = Attendance.objects.filter(
#         student__class_name=assigned_class,
#         date=today
#     ).order_by("student__roll_no")


#     week_history=Attendance.objects.filter(
#         student__class_name=assigned_class,
#         date__range=[start_date,end_date]
#     ).order_by("date","student__roll_no")

#     # CREATE WEEKLY TABLE 
#     students = Student.objects.filter(class_name=assigned_class).order_by("roll_no")

#     attendance_table={}

#     # create empty structure
#     for stu in students:
#         attendance_table[stu] = {}
#         for i in range((end_date - start_date).days + 1):
#             d = start_date + timedelta(days=i)
#             attendance_table[stu][d] = {"morning": "-", "afternoon": "-"}

#     # fill attendance
#     for a in week_history:
#         attendance_table[a.student][a.date][a.session] = a.status

#      # Create date list for template
#     date_list = []
#     if students:
#         sample = next(iter(attendance_table.values()))
#         date_list = list(sample.keys())


#     #  CALCULATE PERCENTAGE
   
#     student_percent = {}

#     for stu in students:
#         all_records = Attendance.objects.filter(student=stu)
#         total = all_records.count()
#         present = all_records.filter(status="Present").count()
#         percentage = round((present / total) * 100, 2) if total else 0
#         student_percent[stu] = percentage

#     # UPDATE CURRENT DAY ATTENDANCE
   
#     if request.method == "POST":
#         for row in records:
#             new_status = request.POST.get(f"status_{row.id}")
#             row.status = new_status
#             row.save()

#         messages.success(request, "Attendance updated successfully!")
#         return redirect("edit_attendance")

#     return render(request, "attendance_edit.html", {
#         "records": records,
#         "today": today,
#         "start_date": start_date,
#         "end_date": end_date,
#         "attendance_table": attendance_table,
#         "student_percent": student_percent,
#         "date_list":date_list
#     })

    # Load **ALL attendance history** for this class
    # history = Attendance.objects.filter(
    #     student__class_name=assigned_class
    # ).order_by("date", "student__roll_no")

    # # Group by student → date → session
    # attendance_table = {}

    # for h in history:
    #     stu = h.student
    #     if stu not in attendance_table:
    #         attendance_table[stu] = {}

    #     if h.date not in attendance_table[stu]:
    #         attendance_table[stu][h.date] = {"morning": "-", "afternoon": "-"}

    #     attendance_table[stu][h.date][h.session] = h.status

    # if request.method == "POST":
    #     for row in records:
    #         new_status = request.POST.get(f"status_{row.id}")
    #         row.status = new_status
    #         row.save()

    #     messages.success(request, "Attendance updated successfully!")
    #     return redirect("edit_attendance")

    # return render(request, "attendance_edit.html", {
    #     "records": records,
    #     "today": today,
    # })



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




# ATTENDANCE SECTION IN TEACHER DASHBOARD


# SELECT THE SESSION FOR THE  ATTENDANCE MORNING OR THE AFTERNOON

def select_attendance_session(request):
    teacher_email = request.session.get("email")
    teacher = Teacher.objects.filter(temail=teacher_email).first()

    class_assigned = teacher.tassign  

    return render(request, "attendance_select_session.html", {
        "class_name": class_assigned
    })


# MARK THE ATTENDANCE

def mark_attendance(request, session):
    teacher_email = request.session.get("email")
    teacher = Teacher.objects.filter(temail=teacher_email).first()
    class_assigned = teacher.tassign

    today = date.today()

    students = Student.objects.filter(class_name=class_assigned).order_by("roll_no")

    # Load existing attendance (if already marked)
    existing = Attendance.objects.filter(
        date=today,
        session=session,
        student__class_name=class_assigned
    )

    attendance_map = {a.student_id: a.status for a in existing}
# Build list of tuples: student + prefilled status
    students_with_status = []
    for s in students:
        status = attendance_map.get(s.id, "Absent")   # default Absent if not recorded
        students_with_status.append((s, status))

    return render(request, "attendance_mark.html", {
        "session": session,
        "today": today,
        "students_with_status": students_with_status,   # <- pass this
        "class_name": class_assigned,
    })


# SAVE ATTENDANCE

def save_attendance(request):
    if request.method != "POST":
        return redirect("select_attendance_session")

    session = request.POST.get("session")
    class_name = request.POST.get("class_name")

    today = date.today()

    students = Student.objects.filter(class_name=class_name)

    for student in students:
        status = request.POST.get(f"att_{student.id}", "Absent")

        Attendance.objects.update_or_create(
            student=student,
            date=today,
            session=session,
            defaults={
                "status": status,
                "student_name": student.name,
                "student_class": class_name
            }
        )

    messages.success(request, f"{session.capitalize()} attendance saved successfully!")
    # return redirect("mark_attendance", session=session)
    return redirect(f"/teacher/attendance/{session}/")


# VIEW ATTENDANCE SHEET


def view_attendance(request):
    teacher_email = request.session.get("email")
    teacher = Teacher.objects.filter(temail=teacher_email).first()
    class_name = teacher.tassign

    # Default week: last 7 days
    today = date.today()
    start_date = today - timedelta(days=6)
    end_date = today

    # Custom date filter
    if request.GET.get("start") and request.GET.get("end"):
        start_date = datetime.strptime(request.GET["start"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.GET["end"], "%Y-%m-%d").date()

    students = Student.objects.filter(class_name=class_name).order_by("roll_no")

    # Load attendance for week
    records = Attendance.objects.filter(
        student__in=students,
        date__range=(start_date, end_date)
    )

    # Map: (student_id, date, session)
    att_map = {(a.student_id, a.date, a.session): a.status for a in records}

    # Build table rows
    table_rows = []
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    for s in students:
        row = {
            "student": s,
            "cells": [],
            "present": 0,
            "total": 0
        }

        for dt in date_range:
            m = att_map.get((s.id, dt, "morning"), "-")
            a = att_map.get((s.id, dt, "afternoon"), "-")

            # Count %
            if m in ("Present", "Absent"):
                row["total"] += 1
                if m == "Present":
                    row["present"] += 1

            if a in ("Present", "Absent"):
                row["total"] += 1
                if a == "Present":
                    row["present"] += 1

            row["cells"].append({"morning": m, "afternoon": a})

        percentage = round((row["present"] / row["total"]) * 100, 2) if row["total"] else 0
        row["percentage"] = percentage

        table_rows.append(row)

    return render(request, "view_attendance.html", {
        "class_name": class_name,
        "date_range": date_range,
        "rows": table_rows,
        "start": start_date,
        "end": end_date
    })
