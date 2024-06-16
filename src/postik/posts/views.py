from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from .models import Card
from .serializers import CardSerializer


def index(request):
    return render(request, 'posts/index.html')


def card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if 'cart' not in request.session:
        request.session['carts'] = {}

    if str(card.id) not in request.session['carts']:
        request.session['carts'][str(card.id)] = {
            'posts': []
        }
    request.session.modified = True
    context = {
        'card': CardSerializer(card).data,
        'cart': request.session['carts'][str(card.id)],
        'image': card.image,
    }
    return render(request, 'posts/card.html', context)


def post_card(request, card_id, post_id):
    card = get_object_or_404(Card, pk=card_id)
    if str(card_id) not in request.session.get('carts', {}):
        HttpResponseNotFound('Cart not found')

    if post_id not in request.session['carts'][str(card_id)]['posts']:
        posts_id = set(request.session['carts'][str(card_id)]['posts'])
        posts_id.add(post_id)
        request.session['carts'][str(card_id)]['posts'] = list(posts_id)
    else:
        posts_id = set(request.session['carts'][str(card_id)]['posts'])
        posts_id.remove(post_id)
        request.session['carts'][str(card_id)]['posts'] = list(posts_id)

    request.session.modified = True

    context = {
        'card': CardSerializer(card).data,
        'cart': request.session['carts'][str(card.id)],
        'image': card.image,
    }
    return render(request, 'posts/card.html', context)
