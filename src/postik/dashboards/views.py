from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.base import TemplateView

from posts.forms import CardForm, PostForm
from posts.models import Card, Post, CardPost
from .utils.telegram import get_telegram_create_post_link


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class DesignPageView(TemplateView):
    template_name = 'dashboards/design.html'

    def get_context_data(self, **kwargs):
        card = Card.objects.get_or_create(
            user=self.request.user
        )[0]

        user_posts = Post.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
        return {
            'title': 'Дизайн',
            'telegram_create_post_link': get_telegram_create_post_link(),
            'card': card,
            'form_card': CardForm(instance=card),
            'user_posts': user_posts,
            'bot_handler_name': settings.BOT_HANDLER_NAME
        }


@login_required(login_url='users:signup')
def preview_card(request):
    card = get_object_or_404(Card, user=request.user)
    context = {
        'card': card
    }
    return render(request, 'includes/card_body.html', context)


@require_POST
@login_required(login_url='users:signup')
def update_card(request):
    card = get_object_or_404(
        Card,
        user=request.user
    )
    form_card = CardForm(
        request.POST,
        request.FILES,
        instance=card
    )
    if form_card.is_valid():
        if form_card.cleaned_data.get('image'):
            card.image = form_card.cleaned_data.get('image')
            print(123)
            card.save()

        form_card.save()

    context = {
        'form_card': form_card
    }
    return render(request, 'dashboards/includes/design_card_form.html', context)


@login_required(login_url='users:signup')
def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    context = {
        'post': post,
        'bot_handler_name': settings.BOT_HANDLER_NAME
    }
    return render(request, "dashboards/includes/design_post.html", context)


@login_required(login_url='users:signup')
def view_post_body(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    context = {
        'post': post,
    }

    return render(request, 'dashboards/includes/design_post_body.html', context)


@login_required(login_url='users:signup')
def view_post_heading(request, post_id):
    card = get_object_or_404(Card, user=request.user)
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    context = {
        'card': card,
        'post': post,
        'bot_handler_name': settings.BOT_HANDLER_NAME
    }
    return render(request, "dashboards/includes/design_post_heading.html", context)


@require_GET
@login_required(login_url='users:signup')
def view_posts_list(request):
    card = get_object_or_404(
        Card,
        user=request.user
    )
    context = {
        'card': card,
        'bot_handler_name': settings.BOT_HANDLER_NAME
    }
    return render(request, "dashboards/includes/design_posts_list.html", context)


@login_required(login_url='users:signup')
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    form_post = PostForm(
        instance=post
    )
    if request.method == 'POST':
        form_post = PostForm(
            request.POST,
            instance=post
        )
        if form_post.is_valid():
            form_post.save()
            context = {
                'post': post,
                'is_success_edit': True,
            }
            return render(
                request,
                'dashboards/includes/design_post_body.html',
                context
            )

    context = {
        'form_post': form_post,
    }
    return render(request, 'dashboards/includes/design_post_edit.html', context)


@login_required(login_url='users:signup')
def delete_post_card(request, post_id):
    card = get_object_or_404(Card, user=request.user)
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    card.posts.remove(post)
    context = {
        'card': card,
        'post': post,
    }
    return render(request, 'dashboards/includes/design_post_body.html', context)


@login_required(login_url='users:signup')
def add_post_card(request, post_id):
    card = get_object_or_404(Card, user=request.user)
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    card.posts.add(post)
    context = {
        'card': card,
        'post': post,
    }
    return render(request, 'dashboards/includes/design_post_body.html', context)
