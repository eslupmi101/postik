from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from .models import Card, PostPurchase
from .serializers import CardSerializer
from .utils import get_telegram_purchased_posts_link


def index(request):
    return render(request, 'posts/index.html')


def card(request, telegram_username):
    card = get_object_or_404(Card, user__telegram_profile__username=telegram_username)
    context = {
        'card': card,
    }
    return render(request, 'posts/card.html', context)


@login_required()
def post_card(request, card_id, post_id):
    card = get_object_or_404(Card, pk=card_id)
    if str(card_id) not in request.session.get('carts', {}):
        HttpResponseNotFound('Cart not found')

    if post_id not in request.session['carts'][str(card_id)]['posts_id']:
        posts_id = set(request.session['carts'][str(card_id)]['posts_id'])
        posts_id.add(post_id)
        request.session['carts'][str(card_id)]['posts_id'] = list(posts_id)

    else:
        posts_id = set(request.session['carts'][str(card_id)]['posts_id'])
        posts_id.remove(post_id)
        request.session['carts'][str(card_id)]['posts_id'] = list(posts_id)

    request.session.modified = True
    context = {
        'card': CardSerializer(card).data,
        'cart': request.session['carts'][str(card.id)],
        'image': card.image,
    }
    return render(request, 'posts/card.html', context)


@login_required()
def buy_posts(request, card_id):
    if str(card_id) not in request.session.get('carts', {}):
        return HttpResponseNotFound('Cart not found')

    posts_id = request.session['carts'][str(card_id)]['posts_id']
    if not posts_id:
        return HttpResponseNotFound('Posts in cart not found')

    PostPurchase.objects.bulk_create([
        PostPurchase(post_id=post_id, user=request.user)
        for post_id in posts_id
    ])

    request.session['carts'][str(card_id)]['posts_id'] = []
    request.session.modified = True

    return redirect(
        get_telegram_purchased_posts_link(posts_id)
    )
