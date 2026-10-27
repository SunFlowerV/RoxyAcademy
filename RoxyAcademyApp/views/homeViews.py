from django.shortcuts import render


def singleCourse(request):
    data = {
        'header': 'false',
        'topToBottom': 'true',
        'footer': 'false',
    }
    return render(request, "home/singleCourse.html", data)
