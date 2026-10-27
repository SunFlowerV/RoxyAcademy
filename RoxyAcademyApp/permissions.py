from django.contrib.auth.decorators import user_passes_test


def instructor_required(view_func):
    return user_passes_test(
        lambda user: user.is_active and (
            user.is_staff or user.groups.filter(name='Instructor').exists()
        ),
        login_url='login',
    )(view_func)
