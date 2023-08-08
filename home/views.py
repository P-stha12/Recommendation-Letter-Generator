import datetime
from django.db.models.fields import DateTimeField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session

# check old password and new password
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib import messages

import json


# imports from xhtml
from django.http import HttpResponse
from django.template.loader import get_template
#from xhtml2pdf import pisa


# serializers helps to convert queryset into json strings
from django.core import serializers

# sending email
from django.core.mail import send_mail

# to send mail to admin
from django.core.mail import mail_admins


# to create random number for OTP
from random import randint

# Create your views here.


def index(request):
    if request.method == "GET":
        naam = request.COOKIES.get('student')
        if StudentLoginInfo.objects.filter(username__exact=naam).exists():
            student = StudentLoginInfo.objects.get(username__exact=naam)
            teachers = TeacherInfo.objects.filter(department=student.department)
            response =  render(
                    request,
                    "Studentform1.html",
                    {
                        "naam": student.username,
                        "teachers": teachers,
                        "roll": student.roll_number,
                    },
                )
            return response
        user = request.COOKIES.get('username')
        if TeacherInfo.objects.filter(name__exact=user).exists():
                value = 0
                unique = request.COOKIES.get('unique')

                teacher_model = TeacherInfo.objects.get(unique_id=unique)
                generated_dataharu = StudentData.objects.filter(professor__unique_id=unique , is_generated=True)

                dataharu = StudentData.objects.filter(professor__unique_id=unique)
                number = len(dataharu)
                # to check if there is request or not on teachers page
                for data in dataharu:
                    if data.is_generated:
                        value += 1
                datakolength = len(dataharu)
                if datakolength == value:
                    check_value = True
                else:
                    check_value = False
                    # to convert database to json objects
                std_dataharu = serializers.serialize(
                    "json", StudentData.objects.filter(professor__unique_id=unique,is_generated=True)
                )
                non_generated = StudentData.objects.filter(
                    is_generated=False, professor__unique_id=unique
                )

                response = render(
                    request,
                    "Teacher.html",
                    {
                        "all_students": generated_dataharu,
                        "student_list": non_generated,
                        "check_value": check_value,
                        "teacher_number": number,
                        "std_dataharu": std_dataharu,
                        "teacher_model": teacher_model,
                    },
                )
                return response
        
    return render(request, "index.html")


def gallery(request):
    return render(request, "gallery.html")


import textwrap
from fpdf import FPDF
from io import BytesIO as bio
#import fs
from home.forms import StudentForm

def text_to_pdf(text,roll):
    a4_width_mm = 270
    pt_to_mm = 0.35
    fontsize_pt = 11
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = (a4_width_mm / 1*character_width_mm)
    
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', size=fontsize_pt*1.2)
    pdf.cell(0, 10,"Letter of Recommendation ",align='C')
    pdf.set_y(15)
    pdf.set_font(family="Arial", size=fontsize_pt)
    
    splitted = text.split("\n")
    a=0
    for line in splitted:
        lines = textwrap.wrap(line, width_text*1.2)

        if a==0:
            if len(lines) == 0:
                pdf.ln()
                a=a+1
                continue
        else:
            if len(lines) == 0:
                continue
      
         

        for wrap in lines:
            pdf.set_right_margin(25)

            pdf.set_x(25)
            pdf.multi_cell(0, fontsize_mm*1.5, wrap)
            a=a-1
           



    pdf.output("media/letter/"+roll+".pdf", "F")


import re

### xhtml2pdf
def final(request, *args, **kwargs):
    if request.method == "POST":
        textarea1 = request.POST.get("textarea1")
        roll = request.POST.get("roll")
        student = StudentData.objects.get(std__roll_number=roll)
        
        # textarea2 = request.POST.get("textarea2")
        # textarea3 = request.POST.get("textarea3")
        letter=f'''
                \n{textarea1}
        '''
        text_to_pdf(letter,roll)
        student.is_generated = True
        student.reapplied = False
        student.save() 
        # messages.error(request, "Sorry!  The Credentials doesn't match.")
        #send_mail('Recommendation Letter', 'Dear sir, Please find the recommendation letter attached with this mail. Link:127.0.0.1:8000/', 'ioerecoletter@gmail.com', [student.email], fail_silently=False)
        return redirect("media/letter/"+roll+".pdf")

def studentfinal(request, *args, **kwargs):
    if request.method == "POST":
        roll = request.POST.get("roll")
    return redirect("media/letter/"+roll+".pdf")

def registerStudent(request):
    departments = Department.objects.all().values()
    programs = Program.objects.all().values()
    context_dict = { "departments": departments , "programs": programs}
    
    if request.method == "GET":
        naam = request.COOKIES.get('student')
        if StudentLoginInfo.objects.filter(username__exact=naam).exists():
            student = StudentLoginInfo.objects.get(username__exact=naam)
            teachers = TeacherInfo.objects.filter(department=student.department)
            response =  render(
                    request,
                    "Studentform1.html",
                    {
                        "naam": student.username,
                        "teachers": teachers,
                        "roll": student.roll_number,
                    },
                )
            return response
        user = request.COOKIES.get('username')
        if TeacherInfo.objects.filter(name__exact=user).exists():
                value = 0
                unique = request.COOKIES.get('unique')

                teacher_model = TeacherInfo.objects.get(unique_id=unique)
                generated_dataharu = StudentData.objects.filter(professor__unique_id=unique , is_generated=True)

                dataharu = StudentData.objects.filter(professor__unique_id=unique)
                number = len(dataharu)
                # to check if there is request or not on teachers page
                for data in dataharu:
                    if data.is_generated:
                        value += 1
                datakolength = len(dataharu)
                if datakolength == value:
                    check_value = True
                else:
                    check_value = False
                    # to convert database to json objects
                std_dataharu = serializers.serialize(
                    "json", StudentData.objects.filter(professor__unique_id=unique,is_generated=True)
                )
                non_generated = StudentData.objects.filter(
                    is_generated=False, professor__unique_id=unique
                )

                response = render(
                    request,
                    "Teacher.html",
                    {
                        "all_students": generated_dataharu,
                        "student_list": non_generated,
                        "check_value": check_value,
                        "teacher_number": number,
                        "std_dataharu": std_dataharu,
                        "teacher_model": teacher_model,
                    },
                )
                return response
        
    if request.method == "POST":
        usern = request.POST.get("name")
        roll = request.POST.get("roll")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        Pass = request.POST.get("pass")
        confirmPass = request.POST.get("confirmPass")
        depart = request.POST.get("department")
        prog = request.POST.get("program")
        department = Department.objects.get(dept_name=depart)
        program = Program.objects.get(program_name=prog)
        if Pass != confirmPass:
            messages.error(request, "Passwords donot match")
            return render(request, "registerStudent.html", context=context_dict )
            
        try:
            if StudentLoginInfo.objects.filter(roll_number__exact=roll):
                messages.error(request, "Student Already Exists")
                return render(request, "registerStudent.html", context=context_dict )
            else:
                Student = StudentLoginInfo.objects.create(username=usern, 
                roll_number=roll, dob=dob, department=department, program=program, gender=gender, password=make_password(Pass))
                Student.save()
                messages.error(request, "Account Sucessfully Created")
                return render(request, "loginStudent.html")
        except Exception as e:
            messages.error(request, e)
            return render(request, "registerStudent.html", context=context_dict )
    return render(request, "registerStudent.html", context=context_dict )

def loginStudent(request):
    if request.method == "GET":
        naam = request.COOKIES.get('student')
        if StudentLoginInfo.objects.filter(username__exact=naam).exists():
            student = StudentLoginInfo.objects.get(username__exact=naam)
            teachers = TeacherInfo.objects.filter(department=student.department)
            response =  render(
                    request,
                    "Studentform1.html",
                    {
                        "naam": student.username,
                        "teachers": teachers,
                        "roll": student.roll_number,
                    },
                )
            return response
        user = request.COOKIES.get('username')
        if TeacherInfo.objects.filter(name__exact=user).exists():
                value = 0
                unique = request.COOKIES.get('unique')

                teacher_model = TeacherInfo.objects.get(unique_id=unique)
                generated_dataharu = StudentData.objects.filter(professor__unique_id=unique , is_generated=True)

                dataharu = StudentData.objects.filter(professor__unique_id=unique)
                number = len(dataharu)
                # to check if there is request or not on teachers page
                for data in dataharu:
                    if data.is_generated:
                        value += 1
                datakolength = len(dataharu)
                if datakolength == value:
                    check_value = True
                else:
                    check_value = False
                    # to convert database to json objects
                std_dataharu = serializers.serialize(
                    "json", StudentData.objects.filter(professor__unique_id=unique,is_generated=True)
                )
                non_generated = StudentData.objects.filter(
                    is_generated=False, professor__unique_id=unique
                )

                response = render(
                    request,
                    "Teacher.html",
                    {
                        "all_students": generated_dataharu,
                        "student_list": non_generated,
                        "check_value": check_value,
                        "teacher_number": number,
                        "std_dataharu": std_dataharu,
                        "teacher_model": teacher_model,
                    },
                )
                return response
            
    if request.method == "POST":
        naam = request.POST.get("username")
        Pass = request.POST.get("pass")
             # check if user is real
        if StudentLoginInfo.objects.filter(username__exact=naam).exists():
            student = StudentLoginInfo.objects.get(username__exact=naam)
            if not check_password(Pass, student.password):
                messages.error(request, "Sorry!  The Credentials doesn't match.")
                return render(request, "loginStudent.html")
            teachers = TeacherInfo.objects.filter(department=student.department)
            if StudentData.objects.filter(std__username=naam).exists():
                stdnt = StudentData.objects.get(std__username=naam)
                if stdnt.is_generated: 
                    response = render(
                        request,
                        "student_success.html",
                        {
                            "naam": student.username,
                            "roll": student.roll_number,
                            "letter": stdnt.is_generated,
                        },
                    )
                    
                else:
                    messages.error(request, "You are succesfully logged in.")
                    response =  render(
                        request,
                        "Studentform1.html",
                        {
                            "naam": student.username,
                            "teachers": teachers,
                            "roll": student.roll_number,
                        },
                    )

            else:
                messages.error(request, "You are succesfully logged in.")
                response =  render(
                    request,
                    "Studentform1.html",
                    {
                        "naam": student.username,
                        "teachers": teachers,
                        "roll": student.roll_number,
                    },
                )
                
            response.set_cookie('student', student)
            return response

        else:
            messages.error(request, "Sorry!  The Credentials doesn't match.")
            return render(request, "loginStudent.html")
        
    
    return render(request, "loginStudent.html")


@login_required(login_url="/loginTeacher")
def make_letter(request):
    if request.method == "POST":
        roll = request.POST.get("roll")
        teacher_id = request.COOKIES.get("unique")
        teacher_model = TeacherInfo.objects.get(unique_id=teacher_id)

        stu = StudentLoginInfo.objects.get(roll_number=roll)
        student = StudentData.objects.get(name=stu.username)
        paper = Paper.objects.get(student__name=student.name)
        project = Project.objects.get(student__name=student.name)
        university = University.objects.get(student__name=student.name)
        quality = Qualities.objects.get(student__name=student.name)
        academics = Academics.objects.get(student__name=student.name)
        files = Files.objects.get(student__name=student.name)
        teacher_name = student.professor.name


        return render(
            request,
            "formTeacher.html",
            {
                "student": student,
                "roll": roll,
                "paper": paper,
                "project": project,
                "university": university,
                "quality": quality,
                "academics": academics,
                "teacher": teacher_name,
                "teacher_model": teacher_model,
                "files": files, 

            },
        )


def studentform1(request):
    if request.method == "POST":
        naam = request.POST.get("naam")
        uroll = request.POST.get("roll")
        uemail = request.POST.get("university")
        print("uemail: ", uemail)
        uprof = request.POST.get("prof")
        known_year = request.POST.get("yrs")
        
        s_project = request.POST.get("sproject")
        is_project = request.POST.get("is_project")
        
        pro1 = request.POST.get("pro1")
        has_paper = request.POST.get("has_paper")
        title_paper = request.POST.get("paper_title")
        paperlink = request.POST.get("paper_link")

        
        deployed = request.POST.get('deploy')
        intern = request.POST.get('intern')

    
        subjects = Subject.objects.all()
        bisaya = []
        i = 0
        for subject in subjects:
            if request.POST.get("subject" + str(i)) is not None:
                bisaya.append(request.POST.get("subject" + str(i)))
            i = i + 1
        listToStr = ",".join([str(elem) for elem in bisaya])
        x = uprof.split("|")
        id = x[-1]
        if StudentLoginInfo.objects.filter(username=naam).exists():
            stu = StudentLoginInfo.objects.get(username=naam)
            teachers = TeacherInfo.objects.filter(department=stu.department)
            if TeacherInfo.objects.filter(unique_id=id).exists():
                prof = TeacherInfo.objects.get(unique_id=id)
                info = StudentData(
                    name=stu.username,
                    universities=uemail,
                    professor=prof,
                    std=stu,
                    is_pro=is_project,
                    years_taught=known_year,
                    subjects=listToStr,
                    is_paper = has_paper,
                    intern = True if intern == "on" else False,
                )
                
                if StudentData.objects.filter(name=naam).exists():
                    info = StudentData.objects.get(name=naam)
                    info.name=stu.username
                    info.universities=uemail
                    info.professor=prof
                    info.std=stu
                    info.is_pro=is_project
                    info.years_taught=known_year
                    info.subjects=listToStr
                    info.is_paper = has_paper
                    info.intern = True if intern == "on" else False
                    info.save()
                    
                else:
                    info.save()

                project_info = Project(
                    supervised_project = s_project,
                    final_project = pro1,
                    deployed = True if deployed == "on" else False,
                    student = info,
                )
                
                if Project.objects.filter(student = info).exists():
                    project = Project.objects.get(student=info)
                    project.delete()
                    
                project_info.save()
                    
                
                paper_info = Paper(
                    paper_link = paperlink,
                    paper_title = title_paper,
                    student = info,
                )
                
                if Paper.objects.filter(student = info).exists():
                    paper = Paper.objects.get(student=info)
                    paper.delete()

                paper_info.save()
            
            else:
                messages.error(request, "Please select a professor.")
                return render(
                        request,
                        "Studentform1.html",
                        {
                            "naam": stu.username,
                            "teachers": teachers,
                            "roll": stu.roll_number,
                        },
                    )

            return render(request, "Studentform2.html", {'roll':uroll},)

        else:
            messages.error(request, "Please login first")
            return render(request, "loginStudent.html")

    
    messages.error(request, "Please login first")
    return render(request, "loginStudent.html")

def studentform2(request):
    if request.method == "POST" :
        uroll = request.POST.get("roll")
        uuni = request.POST.get("university")
        uni_program = request.POST.get("program_applied")
        uni_deadline = request.POST.get("deadline")
        aca_gpa = request.POST.get("gpa")
        aca_ranking = request.POST.get("tentative_ranking")
        file_transcript = request.FILES.get("transcript")
        file_cv = request.FILES.get("cv")
        file_photo = request.FILES.get('photo')
        #presentation= request.POST.get('presentation')
        extra = request.POST.get('eca')
        #quality = request.POST.get('qual')


        # leaders = request.POST.get('quality1')
        # hardwork = request.POST.get('quality2')
        # social = request.POST.get('quality3')
        # teamwork = request.POST.get('quality4')
        # friendly = request.POST.get('quality5')

    

        stu_info = StudentData.objects.get(std__roll_number=uroll)
        if(stu_info.is_generated):
            stu_info.reapplied = True
            stu_info.save()


        uni_info = University(
            uni_name = uuni,
            uni_deadline = uni_deadline,
            program_applied = uni_program,
            student = stu_info,
        )
        if University.objects.filter(student = stu_info).exists():
            uni = University.objects.get(student=stu_info)
            uni.delete()
            
        uni_info.save()

        academics_info = Academics(
            gpa = aca_gpa,
            tentative_ranking = aca_ranking,
            student = stu_info,
        )
        
        if Academics.objects.filter(student = stu_info).exists():
            academic = Academics.objects.get(student=stu_info)
            academic.delete()
            
        academics_info.save()

        file_info = Files(
            transcript = file_transcript,
            CV = file_cv,
            Photo = file_photo,
            student = stu_info,
        )
        
        if Files.objects.filter(student = stu_info).exists():
            file = Files.objects.get(student=stu_info)
            file.delete()
            
        file_info.save()

        qualities_info = Qualities(
            # leadership = True if leaders == "on" else False,
            # hardworking = True if hardwork == "on" else False,
            # social = True if social == "on" else False,
            # teamwork = True if teamwork == "on" else False,
            # friendly =True if friendly == "on" else False,
            # quality = quality,
            # presentation = presentation,
            extracirricular = extra,
            student = stu_info,
        )
        
        if Qualities.objects.filter(student = stu_info).exists():
            quality = Qualities.objects.get(student=stu_info)
            quality.delete()
            
        qualities_info.save()

    return render(request, "student_success.html",{'roll':uroll})


def loginTeacher(request):
    if request.method == "GET":
        naam = request.COOKIES.get('student')
        if StudentLoginInfo.objects.filter(username__exact=naam).exists():
            student = StudentLoginInfo.objects.get(username__exact=naam)
            teachers = TeacherInfo.objects.filter(department=student.department)
            response =  render(
                    request,
                    "Studentform1.html",
                    {
                        "naam": student.username,
                        "teachers": teachers,
                        "roll": student.roll_number,
                    },
                )
            return response
        user = request.COOKIES.get('username')
        if TeacherInfo.objects.filter(name__exact=user).exists():
                value = 0
                unique = request.COOKIES.get('unique')

                teacher_model = TeacherInfo.objects.get(unique_id=unique)
                generated_dataharu = StudentData.objects.filter(professor__unique_id=unique , is_generated=True)
                reapplied_dataharu = StudentData.objects.filter(professor__unique_id=unique , reapplied=True)

                dataharu = StudentData.objects.filter(professor__unique_id=unique)
                number = len(dataharu)
                # to check if there is request or not on teachers page
                for data in dataharu:
                    if data.is_generated:
                        value += 1
                datakolength = len(dataharu)
                if datakolength == value:
                    check_value = True
                else:
                    check_value = False
                    # to convert database to json objects
                std_dataharu = serializers.serialize(
                    "json", StudentData.objects.filter(professor__unique_id=unique,is_generated=True)
                )
                non_generated = StudentData.objects.filter(
                    is_generated=False, professor__unique_id=unique
                )


                response = render(
                    request,
                    "Teacher.html",
                    {
                        "all_students": generated_dataharu,
                        "reapplied":reapplied_dataharu,
                        "student_list": non_generated,
                        "check_value": check_value,
                        "teacher_number": number,
                        "std_dataharu": std_dataharu,
                        "teacher_model": teacher_model,
                    },
                )
                return response
        return render(request, "loginTeacher.html")
            
    value = 0
    if request.method == "POST":
        usern = request.POST.get("username")
        passwo = request.POST.get("password")
        # check if user is real
        if User.objects.filter(username__exact=usern).exists():
            user = authenticate(username=usern, password=passwo)
            if user is not None:
                login(request, user)
                full_name = request.user.get_full_name()
                x = full_name.split(" ")
                unique = "aman"
                # name = x[0]

                teacher_model = TeacherInfo.objects.get(unique_id=unique)
                generated_dataharu = StudentData.objects.filter(professor__unique_id=unique , is_generated=True)

                dataharu = StudentData.objects.filter(professor__unique_id=unique)
                number = len(dataharu)
                # to check if there is request or not on teachers page
                for data in dataharu:
                    if data.is_generated:
                        value += 1
                datakolength = len(dataharu)
                if datakolength == value:
                    check_value = True
                else:
                    check_value = False
                    # to convert database to json objects
                std_dataharu = serializers.serialize(
                    "json", StudentData.objects.filter(professor__unique_id=unique,is_generated=True)
                )
                reapplied_dataharu = StudentData.objects.filter(professor__unique_id=unique , reapplied=True)
                non_generated = StudentData.objects.filter(
                    is_generated=False, professor__unique_id=unique
                )

                response = render(
                    request,
                    "Teacher.html",
                    {
                        "all_students": generated_dataharu,
                        "reapplied":reapplied_dataharu,
                        "student_list": non_generated,
                        "check_value": check_value,
                        "teacher_number": number,
                        "std_dataharu": std_dataharu,
                        "teacher_model": teacher_model,
                    },
                )
                response.set_cookie("unique", unique)
                response.set_cookie("username", user.username)
                
                return response
            # A backend authenticated the credentials
            else:
                # No backend authenticated the credentials
                messages.error(request, "Sorry!  The Password doesnot match.")
                return render(request, "loginTeacher.html")
        else:

            messages.error(request, "You are not registered as a professor.")
            return render(request, "loginTeacher.html")
    



def logoutUser(request):
    logout(request)
    response = redirect("/")
    response.delete_cookie('unique')
    response.delete_cookie('csrftoken')
    response.delete_cookie('username')
    response.delete_cookie('OTP_value')
    return response

def logoutStudent(request):
    response = redirect("/")
    response.delete_cookie('student')
    return response

def forgotPassword(request):
    # generating otp so that it is generated only once
    OTP_value = OTP_generator(5)
    response = render(request, "forgotPassword.html")
    response.set_cookie("OTP_value", OTP_value)
    return response


def forgotUsername(request):
    # generating otp so that it is generated only once
    OTP_value = OTP_generator(5)
    response = render(request, "forgotUsername.html")
    response.set_cookie("OTP_value", OTP_value)
    return response


# check email of username is valid or not
def checkEmail(request):
    if request.method == "POST":

        email = request.POST.get("user_email")
        if User.objects.filter(email__exact=email).exists():
            user = User.objects.get(email__exact=email)
            send_mail(
                "UserName ",
                "Your username  is " + user.username,
                "christronaldo9090909@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Username has been sent to your gmail.")
            return redirect("loginTeacher")
        else:
            messages.error(request, "Email is not registered.")
            return redirect("loginTeacher")
    return redirect("loginTeacher")


# OTP
def otp(request):

    if request.method == "POST":
        Usernaam = request.POST.get("username")
        if User.objects.filter(username=Usernaam).exists():
            sir = User.objects.get(username=Usernaam)
            full_name = sir.get_full_name()
            x = full_name.split("/")
            name = x[0]
            id = x[-1]

            if TeacherInfo.objects.filter(unique_id=id).exists():
                master = TeacherInfo.objects.get(unique_id=id)

                OTP_value = request.COOKIES.get("OTP_value")

                send_mail(
                    "OTP ",
                    "Your OTP for Recoomendation Letter is " + str(OTP_value),
                    "recoioe@gmail.com",
                    [master.email],
                    fail_silently=False,
                )

                response = render(
                    request,
                    "otp.html",
                    {"teacherkonam": master, "OTP_value": OTP_value},
                )
                # making cookies to store and send them to other view page

                response.set_cookie("teacher_ko_naam", master)
                response.set_cookie("teacher_ko_user", Usernaam)
                return response

            else:
                messages.error(request, "Sorry You are not registered as a Professor.")
                return render(request, "loginTeacher.html")

        else:
            messages.error(request, "Sorry You are not registered as a Professor.")
            return render(request, "loginTeacher.html")


# Otp check
def OTP_check(request):
    if request.method == "POST":
        user_OTP_value = request.POST.get("user_typed_OTP_value")

        # using cookies to obtain otp value and teacher
        OTP_value = request.COOKIES.get("OTP_value")
        teacher_ko_naam = request.COOKIES.get("teacher_ko_naam")

        if OTP_value == user_OTP_value:
            return render(
                request, "validatePassword.html", {"teacher_ko_naam": teacher_ko_naam}
            )
        else:
            messages.error(request, "Wrong OTP_value")
            return render(request, "loginTeacher.html")


# #to pass the username and to validate the user

# def validatePassword(request):
#     teacher_ko_naam=request.COOKIES.get('teacher_ko_naam')
#     OTP_value=request.COOKIES.get('OTP_value')
#     return render(request, 'validatePassword.html',{'teacher_ko_naam':teacher_ko_naam, 'OTP_value':OTP_value})


# pwd is changed of corresponding user passed from validatePassword
def changePassword(request):

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

    if password1 == password2:
        # Teacher ko Username using cookies from 'otp' view page
        teacher_ko_user_naam = request.COOKIES.get("teacher_ko_user")

        # changing Pwd
        usr = User.objects.get(username=teacher_ko_user_naam)
        usr.set_password(password1)
        usr.save()
        messages.success(request, "Password has been changed successfully.")
        return render(request, "loginTeacher.html")
    else:

        return render(request, "validatePassword.html")


def OTP_generator(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


# to pass message to admin user
def contact(request):

    return render(request, "contact.html")


def about(request):

    return render(request, "about.html")


def feedback(request):

    if request.method == "POST":
        First_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        feedback = request.POST.get("feedback")

        message = (
            str(First_name)+" " 
            + str(last_name)
            + "\n"
            + str(email)
            + "\n"
            + str(feedback)
        )

        mail_admins(
            "Feedback", message, fail_silently=False, connection=None, html_message=None
        )
        send_mail(
            "Reply From Recoomendation Letter Team",
            "Thank you for your feedback. We will get back to you soon.",
            " christronaldo9090909@gmail.com",
            [email],
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent.")
        return render(request, "contact.html")


def userDetails(request):
    subject=[]
    naya_subjects=[]
    unique = request.COOKIES.get("unique")
   
    
    teacherkonam = TeacherInfo.objects.get(unique_id=unique)
    email = teacherkonam.email
    username = User.objects.get(email=email)
    subjects=teacherkonam.subjects.all()
    length = len(subjects)
    bisaya=Subject.objects.all()
    
    for i in bisaya:
        if i not in subjects:
            naya_subjects.append(i)
        else:
            subject.append(i)
    
    return render(
        request,
        "userDetails.html",
        {"teacher_username": username, "teacher": teacherkonam,'subjects':subject,'bisaya':bisaya, 'length':length},
    )
    
def studentDetails(request):
    student = request.COOKIES.get("student")
    if StudentLoginInfo.objects.filter(username__exact = student).exists():
        student = StudentLoginInfo.objects.get(username__exact = student)
        return render(
            request,
            "studentDetails.html",
            {"username": student.username,'roll':student.roll_number, 'department': student.department,'program': student.program,'gender': student.gender,
            'dob': student.dob},
        )
    else:
        return render(
            request,
            "studentDetails.html")

def studentDetailTeacher(request, roll):
    student = roll
    if StudentLoginInfo.objects.filter(roll_number = roll).exists():
        student = StudentLoginInfo.objects.get(roll_number = student)
        alt = StudentData.objects.get(std__roll_number=student.roll_number)
        print("universtities: ", alt.universities)
        return render(
            request,
            "studentDetailTeacher.html",
            {"username": student.username,'roll':student.roll_number, 'department': student.department,'program': student.program,'gender': student.gender,
            'dob': student.dob, 'universities': alt.universities},
        )
    else:
        return render(
            request,
            "studentDetailTeacher.html")
    
def profileUpdate(request):
    unique = request.COOKIES.get("unique")
    teacherkonam = TeacherInfo.objects.get(unique_id=unique)

    return render(request, "profileUpdate.html", {"teacher": teacherkonam})


def profileUpdateRequest(request):

    unique = request.COOKIES.get("unique")
    teacherkonam = TeacherInfo.objects.get(unique_id=unique)
    email = teacherkonam.email
    username = User.objects.get(email=email)

    if request.method == "POST":
        photo = request.FILES["file"]

        # TeacherInfo.objects.filter(unique_id=unique).update(images=photo)

        teacherkonam = TeacherInfo.objects.get(unique_id=unique)
        teacherkonam.images = photo
        teacherkonam.save()

    return render(request, "userDetails.html", {"teacher_username": username, "teacher": teacherkonam})


def changeUsername(request):
    if request.method == "POST":
        old_username = request.POST.get("old_username")
        new_username = request.POST.get("new_username")

        if User.objects.filter(username=old_username).exists():
            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists.")
                return redirect(userDetails)

            user = User.objects.get(username=old_username)
            user.username = new_username
            user.save()
            messages.success(request, "Username has been changed successfully.")
            return redirect(loginTeacher)
        else:
            messages.error(request, "No such username exists. ")
    return redirect(userDetails)

def changeStudentName(request):
    if request.method == "POST":
        old_username = request.POST.get("old_username")
        new_username = request.POST.get("new_username")

        if StudentLoginInfo.objects.filter(username=old_username).exists():
            if StudentLoginInfo.objects.filter(username=new_username).exists():
                messages.error(request, "Student already exists.")
                return redirect(studentDetails)

            student = StudentLoginInfo.objects.get(username=old_username)
            student.username = new_username
            student.save()
            messages.success(request, "Your username has been changed successfully.")
            response = redirect(loginStudent)
            response.delete_cookie('student')
            return response
        else:
            messages.error(request, "No such student exists. ")
            return redirect(studentDetails)
    return redirect(studentDetails)


# to change the password of the corresponding user within website
@login_required(login_url="/loginTeacher")
def userPasswordChange(request):
    if request.method == "POST":
        typed_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # to obtain old password,
        user = User.objects.get(username=request.COOKIES.get("username"))
        current_password = request.user.password

        # confirming typed old password is true or not
        old_new_check = check_password(typed_password, current_password)
        if old_new_check:
            if new_password == confirm_password:
                user = User.objects.get(username=request.COOKIES.get("username"))
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been changed successfully.")
                return redirect(loginTeacher)
            else:
                messages.error(request, "Password does not match.")
                return redirect(userDetails)
        else:
            messages.error(request, "Old Password didnt match")
            return redirect(userDetails)

# to change the password of the corresponding student within website
@login_required(login_url="/loginStudent")
def studentPasswordChange(request):
    if request.method == "POST":
        typed_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # to obtain old password,
        student = StudentLoginInfo.objects.get(username=request.COOKIES.get("student"))
        current_password = student.password

        # confirming typed old password is true or not
        old_new_check = check_password(typed_password, current_password)
        if old_new_check:
            if new_password == confirm_password:
                student = StudentLoginInfo.objects.get(username=student)
                student.password = make_password(new_password)
                student.save()
                response = redirect(loginStudent)
                messages.success(request, "Password has been changed successfully.")
                response.delete_cookie('student')
                return response
            else:
                messages.error(request, "Passwords do not match.")
                return redirect(studentDetails)
        else:
            messages.error(request, "Old Password didn't match")
            return redirect(studentDetails)


def changeTitle(request):
    if request.method == "POST":
        new_title = request.POST.get("new_title")
        usernaam = request.COOKIES.get("username")

        user = User.objects.get(username=usernaam)
        full_name = user.get_full_name()
        x = full_name.split("/")

        unique = x[-1]

        if TeacherInfo.objects.filter(unique_id=unique).exists():
            teacher = TeacherInfo.objects.get(unique_id=unique)
            teacher.title = new_title
            teacher.save()

            messages.success(request, "Title has been changed successfully.")
            return redirect(userDetails)
        else:
            messages.error(request, "No such Teacher exists. ")
            return redirect(userDetails)

    return redirect(userDetails)


def changePhone(request):
    if request.method == "POST":
        new_phone = request.POST.get("new_phone")
        usernaam = request.COOKIES.get("username")

        user = User.objects.get(username=usernaam)
        full_name = user.get_full_name()
        x = full_name.split("/")

        unique = x[-1]

        if TeacherInfo.objects.filter(unique_id=unique).exists():
            teacher = TeacherInfo.objects.get(unique_id=unique)
            teacher.phone = new_phone
            teacher.save()

            messages.success(request, "Phone Number has been changed successfully.")
            return redirect(userDetails)
        else:
            messages.error(request, "No such Teacher exists. ")
            return redirect(userDetails)

    return redirect(userDetails)


def changeEmail(request):
    if request.method == "POST":
        new_email = request.POST.get("new_email")
        usernaam = request.COOKIES.get("username")

        user = User.objects.get(username=usernaam)
        full_name = user.get_full_name()
        x = full_name.split("/")

        unique = x[-1]

        if TeacherInfo.objects.filter(unique_id=unique).exists():
            teacher = TeacherInfo.objects.get(unique_id=unique)
            teacher.email = new_email
            teacher.save()

            user = User.objects.get(username=usernaam)
            user.email = new_email
            user.save()

            messages.success(request, "Email has been changed successfully.")
            return redirect(userDetails)
        else:
            messages.error(request, "No such Teacher exists. ")
            return redirect(userDetails)

    return redirect(userDetails)

def addSubjects(request):
    if request.method == "POST":
        subject= request.POST.get("subject")
        usernaam = request.COOKIES.get("username")

        user = User.objects.get(username=usernaam)
        full_name = user.get_full_name()
        x = full_name.split("/")

        unique = x[-1]
      
        if TeacherInfo.objects.filter(unique_id=unique).exists():
            teacher = TeacherInfo.objects.get(unique_id=unique)
            naya_subject=Subject.objects.get(name=subject)
            # to check if subject is in teacher model or not
            check=[]
            subjects=teacher.subjects.all()
            for i in subjects:
                check.append(i.name)
            
            if subject in check:
                messages.error(request, "Subject already exists.")
                return redirect(userDetails)
        
            else:
                teacher.subjects.add(naya_subject)
                messages.success(request, "Subject has been added successfully.")
                return redirect(userDetails)
        else:
            messages.error(request, "No such Subject exists. ")
            return redirect(userDetails)

    return redirect(userDetails)

def deleteSubjects(request):
   
    if request.method == "POST":
        subject= request.POST.get("subject")
        usernaam = request.COOKIES.get("username")

        user = User.objects.get(username=usernaam)
        full_name = user.get_full_name()
        x = full_name.split("/")

        unique = x[-1]
      
        if TeacherInfo.objects.filter(unique_id=unique).exists():
            teacher = TeacherInfo.objects.get(unique_id=unique)
            naya_subject=Subject.objects.get(name=subject)

            # to check if subject is in teacher model or not
            check=[]
            subjects=teacher.subjects.all()
            for i in subjects:
                check.append(i.name)
            if subject not in check:
               
                messages.error(request, "Subject does not exists.")
                return redirect(userDetails)
        
            else:
                teacher.subjects.remove(naya_subject)
                messages.success(request, "Subject has been removed successfully.")
                return redirect(userDetails)
        else:
            messages.error(request, "No such Subject exists. ")
            return redirect(userDetails)

    return redirect(userDetails)

# for dynamic dropdown of subjects
def getdetails(request):
    teacher_id = json.loads(request.GET.get("d_name"))
    result_set = []

    teacher = TeacherInfo.objects.get(unique_id=teacher_id)
    subjects = teacher.subjects.all()

    for subject in subjects:
        result_set.append({"subject_name": subject})
    return HttpResponse(
        json.dumps(result_set, indent=4, sort_keys=True, default=str),
        content_type="application/json",
    )


# edit letter of recommendation
def edit(request):
    if request.method == "POST":
        roll = request.POST.get("roll")

        presentation= request.POST.get('presentation')
        quality = request.POST.get('qual')

        leaders = request.POST.get('quality1')
        hardwork = request.POST.get('quality2')
        social = request.POST.get('quality3')
        teamwork = request.POST.get('quality4')
        friendly = request.POST.get('quality5')

        recommend = request.POST.get('recommend')

        stu_info = StudentData.objects.get(std__roll_number=roll)


        # qualities_info = Qualities(
        #     leadership = True if leaders == "on" else False,
        #     hardworking = True if hardwork == "on" else False,
        #     social = True if social == "on" else False,
        #     teamwork = True if teamwork == "on" else False,
        #     friendly =True if friendly == "on" else False,
        #     quality = quality,
        #     presentation = presentation,
        #     recommend = recommend,
        #     #extracirricular = extra,
        #     student = stu_info,
        # )
        # qualities_info.save(update_fields=["leadership", "hardworking", 
        # "social", "teamwork", "friendly", "quality", "presentation", "recommend" , "student"])

        Qualities.objects.filter(student = stu_info).update(leadership = True if leaders == "on" else False,
                                                            hardworking = True if hardwork == "on" else False,
                                                            social = True if social == "on" else False,
                                                            teamwork = True if teamwork == "on" else False,
                                                            friendly =True if friendly == "on" else False,
                                                            quality = quality,
                                                            presentation = presentation,
                                                            recommend = recommend,)


        #student = StudentData.objects.get(std__roll_number = roll)
        stu = StudentLoginInfo.objects.get(roll_number=roll)
        student = StudentData.objects.get(name=stu.username)
        paper = Paper.objects.get(student__name=student.name)
        project = Project.objects.get(student__name=student.name)
        university = University.objects.get(student__name=student.name)
        quality = Qualities.objects.get(student__name=student.name)
        academics = Academics.objects.get(student__name=student.name)
        teacher_name = student.professor.name
        files = Files.objects.get(student__name=student.name)

        bisaya=student.subjects
        
        subjec=bisaya.split(',')
        subjects=subjec[:-1]
        subject=subjec[-1]

        #student firstname
        name = student.name
        fname = name.split(' ')
        firstname = fname[0]
        

        length=len(subjec)
        if length==1:
            value=True
        else:
            value=False

        return render(request, 
                        "test.html", 
                        {
                            "student": student,
                            'subjects':subjects,
                            'subject':subject,
                            'value':value , 
                            'firstname':firstname,
                            "paper": paper,
                            "project": project,
                            "university": university,
                            "quality": quality,
                            "academics": academics,
                            "teacher": teacher_name,
                            "files": files, 
                        }
                    )


def testing(request):
    if request.method == "POST":
        textarea = request.POST.get("textarea")
    return render(request, "testing.html", {"letter": textarea})


def teacher(request):
    value=0
   
    unique = request.COOKIES.get("unique")

    teacher_model = TeacherInfo.objects.get(unique_id=unique)
    # for loop launlaii 
    generated_dataharu = StudentData.objects.filter(professor__unique_id=unique , is_generated=True)

    dataharu = StudentData.objects.filter(professor__unique_id=unique)
    reapplied_dataharu = StudentData.objects.filter(professor__unique_id=unique, reapplied=True)
    print("yeta aayo", reapplied_dataharu)

    number = len(dataharu)
    # to check if there is request or not on teachers page
    for data in dataharu:
        if (data.is_generated and not(data.reapplied)):
            value += 1
    datakolength = len(dataharu)
    if datakolength == value:
        check_value = True
    else:
        check_value = False
        # to convert database to json objects
    std_dataharu = serializers.serialize(
        "json", StudentData.objects.filter(professor__unique_id=unique,is_generated=True)
    )
    non_generated = StudentData.objects.filter(
        is_generated=False, professor__unique_id=unique
    )

    response = render(
        request,
        "Teacher.html",
        {
            "all_students": generated_dataharu,
            "reapplied": reapplied_dataharu,
            "student_list": non_generated,
            "check_value": check_value,
            "teacher_number": number,
            "std_dataharu": std_dataharu,
            "teacher_model": teacher_model,
        },
    )
    return response

