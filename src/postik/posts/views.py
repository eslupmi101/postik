from django.shortcuts import get_object_or_404, render

from .models import Card


def index(request):
    return render(request, 'posts/index.html')


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
