from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from RoxyAcademyApp.forms import CourseForm
from RoxyAcademyApp.models import Course
from RoxyAcademyApp.permissions import instructor_required


def courseDetails(request):
    data = {
        'footer':'false',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"courses/courseDetails.html",data)

def courseDetails2(request):
    data = {
        'footer':'true',
        'topToBottom':'true',
        'bodyClass':'',
    }
    return render(request,"courses/courseDetails2.html",data)

def courseDetails3(request):
    data = {
        'footer':'true',
        'bodyClass':'',
    }
    return render(request,"courses/courseDetails3.html",data)


def _course_editor_context(course, form=None):
    return {
        'topToBottom': 'true',
        'footer': 'false',
        'form': form or CourseForm(instance=course),
        'is_edit': True,
        'course': course,
    }


@instructor_required
def createCourse(request, course_id=None):
    course = None
    if course_id is not None:
        course = get_object_or_404(Course, pk=course_id, author=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            if course.pk is None:
                course.author = request.user
            course.save()
            if course_id is None:
                messages.success(request, 'Курс сохранён как черновик.')
            else:
                messages.success(request, 'Изменения курса сохранены.')
            return redirect('instructorCourse')
    else:
        form = CourseForm(instance=course)

    if course is not None:
        data = _course_editor_context(course, form=form)
    else:
        data = {
            'topToBottom': 'true',
            'footer': 'false',
            'form': form,
            'is_edit': False,
            'course': None,
        }
    return render(request, "courses/createCourse.html", data)


@instructor_required
def instructorCourse(request):
    data = {
        'footer':'true',
        'bodyClass':'',
        'published_courses': Course.objects.filter(
            author=request.user,
            status=Course.STATUS_PUBLISHED,
        ),
        'archived_courses': Course.objects.filter(
            author=request.user,
            status=Course.STATUS_ARCHIVED,
        ),
        'draft_courses': Course.objects.filter(
            author=request.user,
            status=Course.STATUS_DRAFT,
        ),
    }
    return render(request,"dashboard/InstructorDashboard/instructorCourses.html",data)

def lesson(request):
    return render(request, "courses/lesson.html", {
        'header': 'false',
        'topToBottom': 'false',
        'footer': 'false',
    })
