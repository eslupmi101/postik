from django.shortcuts import get_object_or_404, render

from .models import Card


def index(request):
    context = {
        'title': 'POSTIK',
        'description': 'POSTIK — это инструмент, позволяющий вам зарабатывать на ваших постах.'
    }
    return render(request, 'posts/index.html', context)


def card(request, telegram_username):
    card = get_object_or_404(
        Card,
        user__telegram_profile__username=telegram_username,
        is_active=True
    )
    context = {
        'card': card,
        'title': telegram_username,
    }
    return render(request, 'posts/card.html', context)
