from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_POST

from posts.models import Card, Post
from posts.serializers import PostSerializer
from .forms import CardForm
from .utils.sessions import (add_post_session,
                             delete_post_session,
                             update_post_session)
from .utils.images import convert_to_base64, convert_from_base64


# Design page
@login_required(login_url='users:signup')
def design(request):
    if 'card' not in request.session:
        card = Card.objects.get_or_create(user=request.user)[0]

        card_data = {
            'id': card.id,
            'title': card.title,
            'description': card.description,
            'image': convert_to_base64(card.image),
            'posts': [
                PostSerializer(post).data for post in Post.objects.filter(user=request.user, cards=card).all()
            ],
            # id - int
            'id_selected_posts': []
        }
        request.session['card'] = card_data

    context = {
        'title': 'Дизайн',
        'card': request.session['card'],
        'is_preview': True
    }
    return render(request, 'dashboards/design.html', context)


@login_required(login_url='users:signup')
def modal_posts(request):
    if request.POST.get('post_id'):
        instance = Post.objects.filter(
            id=request.POST.get('post_id'),
            user=request.user,
            is_active=True
        )
        # Delete or Add post to session
        if instance.exists():
            post = PostSerializer(instance.first()).data
            is_post_in_session = any(
                post_session['id'] == post['id'] for post_session in request.session['card']['posts']
            )
            if is_post_in_session:
                request.session['card'] = delete_post_session(request.session['card'], post['id'])
            else:
                request.session['card'] = add_post_session(request.session['card'], post)
            request.session.modified = True

    posts_list = Post.objects.filter(user=request.user).order_by('created_at').all()
    context = {
        'card': request.session['card'],
        'posts': posts_list,
        'is_preview': True
    }

    return render(request, 'dashboards/design/modal.html', context)


@login_required(login_url='users:signup')
def card_posts(request):
    context = {
        'card': request.session['card'],
        'is_preview': True
    }
    return render(request, 'dashboards/design/card-posts.html', context=context)


@login_required(login_url='users:signup')
def preview_card(request):
    context = {
        'card': request.session['card'],
        'is_preview': True
    }
    return render(request, 'posts/card.html', context=context)


@require_POST
@login_required(login_url='users:signup')
def update_card(request):
    session_card = request.session.get('card', {})

    if request.POST.get('title'):
        session_card['title'] = request.POST.getlist('title')[0]

    if request.POST.get('description'):
        session_card['description'] = request.POST.getlist('description')[0]

    if 'avatar' in request.FILES:
        session_card['image'] = convert_to_base64(request.FILES['avatar'])

    request.session['card'] = session_card
    request.session.modified = True
    print(session_card['image'])

    context = {
        'title': 'Дизайн',
        'card': request.session['card'],
        'is_preview': True
    }
    return render(request, 'posts/card.html', context)


@require_POST
@login_required(login_url='users:signup')
def update_post(request, post_id):
    instance = Post.objects.filter(
        id=post_id,
        user=request.user,
        is_active=True
    )

    if not instance.exists():
        return HttpResponseNotFound('Post not found')

    post = instance.first()

    # сделать через форму
    if request.POST.get('image'):
        post.image = request.POST.get('image')

    if request.POST.get('title'):
        post.title = request.POST.get('title')

    if request.POST.get('description'):
        post.description = request.POST.get('description')

    if request.POST.get('price'):
        print(request.POST.get('price'))
        post.price = Decimal(request.POST.get('price'))

    post.save()

    request.session['card'] = update_post_session(
        request.session['card'],
        [post]
    )
    request.session.modified = True

    context = {
        'card': request.session['card'],
        'is_preview': True
    }
    return render(request, 'posts/card.html', context=context)


@require_POST
@login_required(login_url='users:signup')
def save_card(request):
    if not request.session.get('card'):
        return HttpResponseNotFound('Card not found')

    card_data = dict(request.session['card'])
    posts_ids = [post['id'] for post in card_data.get('posts', [])]
    card_data['posts'] = posts_ids
    form = CardForm(card_data, user=request.user)

    context = {
        'form': form,
        'success': False,
        'is_preview': True
    }
    if form.is_valid():
        card = Card.objects.get(user=request.user)
        card.title = form.cleaned_data['title']
        card.description = form.cleaned_data['description']
        card.image = convert_from_base64(card_data['image'])
        card.posts.set(form.cleaned_data['posts'])
        card.save()
        context['success'] = True

    return render(request, 'dashboards/includes/save-card.html', context=context)


# Connect page
@login_required(login_url='users:signup')
def connect(request):
    context = {
        'title': 'Подключение',
    }
    return render(request, 'dashboards/connect.html', context=context)
