from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


INSTRUCTOR_GROUP = 'Instructor'


def _redirect_after_login(user):
    if user.is_staff:
        return redirect('/admin/')
    if user.groups.filter(name=INSTRUCTOR_GROUP).exists():
        return redirect('instructorDashboard')
    return redirect('studentDashboard')


def _get_user_by_identifier(identifier):
    if not identifier:
        return None
    return (
        User.objects.filter(username__iexact=identifier).first()
        or User.objects.filter(email__iexact=identifier).first()
    )


def login_view(request):
    if request.user.is_authenticated:
        return _redirect_after_login(request.user)

    if request.method == 'POST':
        username_or_email = (
            request.POST.get('username')
            or request.POST.get('con_name')
            or request.POST.get('con_email')
        )
        password = request.POST.get('password') or request.POST.get('con_password')

        if not username_or_email or not password:
            messages.error(request, 'Введите логин и пароль.')
        else:
            user = _get_user_by_identifier(username_or_email)
            if user is None:
                messages.error(request, 'Пользователь не найден.')
            else:
                authenticated_user = authenticate(request, username=user.username, password=password)
                if authenticated_user is None:
                    messages.error(request, 'Неверный пароль.')
                else:
                    login(request, authenticated_user)
                    messages.success(request, f'Добро пожаловать, {authenticated_user.username}!')
                    return _redirect_after_login(authenticated_user)

    data = {
        'topToBottom': 'true',
        'bodyClass': 'rbt-header-sticky',
        'footer': 'false',
    }
    return render(request, 'pages/login.html', data)


def register_view(request):
    if request.user.is_authenticated:
        return _redirect_after_login(request.user)

    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('register_user')
        email = request.POST.get('email') or request.POST.get('register-email')
        password = request.POST.get('password1') or request.POST.get('register_password')
        confirm_password = request.POST.get('password2') or request.POST.get('register_conpassword')
        role = request.POST.get('role', 'user')

        if not username or not email or not password or not confirm_password:
            messages.error(request, 'Заполните все поля регистрации.')
        elif role not in {'user', 'student'}:
            messages.error(request, 'Выберите допустимый тип пользователя.')
        elif password != confirm_password:
            messages.error(request, 'Пароли не совпадают.')
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)
            messages.success(request, 'Регистрация успешно завершена.')
            return _redirect_after_login(user)

    data = {
        'topToBottom': 'true',
        'bodyClass': 'rbt-header-sticky',
        'footer': 'false',
    }
    return render(request, 'pages/login.html', data)


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')
