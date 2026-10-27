from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from RoxyAcademyApp.permissions import instructor_required


@instructor_required
def instructorAnnouncements(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorAnnouncements.html",data)


@instructor_required
def instructorAssignments(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"dashboard/InstructorDashboard/instructorAssignments.html",data)


@instructor_required
def instructorDashboard(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorDashboard.html",data)


@instructor_required
def instructorEnrolledCourses(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorEnrolledCourses.html",data)


@instructor_required
def instructorMyQuizAttempts(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
    }
    return render(request,"dashboard/InstructorDashboard/instructorMyQuizAttempts.html",data)


@instructor_required
def instructorOrderHistory(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorOrderHistory.html",data)


@instructor_required
def instructorProfile(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorProfile.html",data)


@instructor_required
def instructorQuizAttempts(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorQuizAttempts.html",data)


@instructor_required
def instructorReviews(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorReviews.html",data)


@instructor_required
def instructorSettings(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/InstructorDashboard/instructorSettings.html",data)


@login_required(login_url='login')
def studentDashboard(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentDashboard.html",data)


@login_required(login_url='login')
def studentEnrolledCourses(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentEnrolledCourses.html",data)


@login_required(login_url='login')
def studentMyQuizAttempts(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentMyQuizAttempts.html",data)


@login_required(login_url='login')
def studentOrderHistory(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentOrderHistory.html",data)


@login_required(login_url='login')
def studentProfile(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentProfile.html",data)


@login_required(login_url='login')
def studentReviews(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentReviews.html",data)


@login_required(login_url='login')
def studentSettings(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"dashboard/studentDashboard/studentSettings.html",data)

