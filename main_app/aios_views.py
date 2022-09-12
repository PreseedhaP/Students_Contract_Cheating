import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def aios_home(request):
    aios = get_object_or_404(Aios, admin=request.user)
    context = {

    }
    return render(request, 'aios_template/home_content.html', context)


def aios_take_attendance(request):
    aios = get_object_or_404(Aios, admin=request.user)
    subjects = Subject.objects.filter(aios_id=aios)
    context = {
        'subjects': subjects,
        'page_title': 'Take Attendance'
    }

    return render(request, 'aios_template/aios_take_attendance.html', context)

@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        students = Student.objects.filter(
            course_id=subject.course.id)
        student_data = []
        for student in students:
            data = {
                    "id": student.id,
                    "name": student.admin.last_name + " " + student.admin.first_name
                    }
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def save_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    students = json.loads(student_data)
    try:
        session = get_object_or_404(Session, id=session_id)
        subject = get_object_or_404(Subject, id=subject_id)
        attendance = Attendance(session=session, subject=subject, date=date)
        attendance.save()

        for student_dict in students:
            student = get_object_or_404(Student, id=student_dict.get('id'))
            attendance_report = AttendanceReport(student=student, attendance=attendance, status=student_dict.get('status'))
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def aios_update_attendance(request):
    aios = get_object_or_404(Aios, admin=request.user)
    subjects = Subject.objects.filter(aios_id=aios)
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Update Attendance'
    }

    return render(request, 'aios_template/aios_update_attendance.html', context)


@csrf_exempt
def get_student_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        student_data = []
        for attendance in attendance_data:
            data = {"id": attendance.student.admin.id,
                    "name": attendance.student.admin.last_name + " " + attendance.student.admin.first_name,
                    "status": attendance.status}
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    students = json.loads(student_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for student_dict in students:
            student = get_object_or_404(
                Student, admin_id=student_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
            attendance_report.status = student_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")

def aios_apply_leave(request):
    form = LeaveReportStaffForm(request.POST or None)
    aios = get_object_or_404(Aios, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportAios.objects.filter(aios=aios),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.aios = aios
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('aios_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "aios_template/aios_apply_leave.html", context)


def aios_feedback(request):
    form = FeedbackAiosForm(request.POST or None)
    aios = get_object_or_404(Aios, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackAios.objects.filter(aios=aios),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.aios = aios
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('aios_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "aios_template/aios_feedback.html", context)

def aios_view_profile(request):
    aios = get_object_or_404(Aios, admin=request.user)
    form = AiosEditForm(request.POST or None, request.FILES or None,instance=aios)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = aios.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                aios.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('aios_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "aios_template/aios_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "aios_template/aios_view_profile.html", context)

    return render(request, "aios_template/aios_view_profile.html", context)


@csrf_exempt
def aios_fcmtoken(request):
    token = request.POST.get('token')
    try:
        aios_user = get_object_or_404(CustomUser, id=request.user.id)
        aios_user.fcm_token = token
        aios_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def aios_view_notification(request):
    aios = get_object_or_404(Aios, admin=request.user)
    notifications = NotificationAios.objects.filter(aios=aios)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "aios_template/aios_view_notification.html", context)


def aios_add_result(request):
    aios = get_object_or_404(Aios, admin=request.user)
    subjects = Subject.objects.filter(aios=aios)

    context = {
        'page_title': 'Result Upload',
        'subjects': subjects
    }
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_list')
            subject_id = request.POST.get('subject')
            test = request.POST.get('test')
            exam = request.POST.get('exam')
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            try:
                data = StudentResult.objects.get(
                    student=student, subject=subject)
                data.exam = exam
                data.test = test
                data.save()
                messages.success(request, "Scores Updated")
            except:
                result = StudentResult(student=student, subject=subject, test=test, exam=exam)
                result.save()
                messages.success(request, "Scores Saved")
        except Exception as e:
            messages.warning(request, "Error Occured While Processing Form")
    return render(request, "aios_template/aios_add_result.html", context)


@csrf_exempt
def fetch_student_result(request):
    try:
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        result = StudentResult.objects.get(student=student, subject=subject)
        result_data = {
            'exam': result.exam,
            'test': result.test
        }
        return HttpResponse(json.dumps(result_data))
    except Exception as e:
        return HttpResponse('False')
