from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .utils import generate_qr_code_svg, get_telegram_auth_link


def auth_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboards:design'))

    telegram_auth_link = get_telegram_auth_link(request)
    auth_qr_code_svg = generate_qr_code_svg(telegram_auth_link)

    context = {
        'telegram_auth_link': telegram_auth_link,
        'auth_qr_code_svg': auth_qr_code_svg
    }

    return render(request, 'users/auth.html', context)


def logout_view(request):
    logout(request)
    return redirect('posts:index')
