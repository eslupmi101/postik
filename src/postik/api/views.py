import logging

from django.db.models import Q
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, resolve_url
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from users.models import TelegramProfile, User
from .permissions import (AuthTelegramCheckPermission,
                          BotHandlerTokenPermission, BotManagerTokenPermission)
from .serailizers import (PostCreateSerializer, PostPurchaseSerializer,
                          TelegramProfileSerializer, LeadSerializer)


class BotManagerAuthView(APIView):
    permission_classes = [BotManagerTokenPermission]

    def post(self, request, *args, **kwargs):
        """
        Create or get user and save telegram_id in session.

        Bot manager send django session_id of user
        and his telegram id and username

        Combine telegram and session data to authorize or register a user.
        Save the telegram ID in the session
        """
        # Validate session_id
        instance_session_key = Session.objects.filter(session_key=request.data['session_id'])
        if not instance_session_key.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'session_id': 'Invalid session_id'
                }
            )
        session = SessionStore(session_key=request.data['session_id'])

        serializer = TelegramProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not TelegramProfile.objects.filter(telegram_id=serializer.validated_data['telegram_id']).exists():
            user = User.objects.create_user(
                username=serializer.validated_data['username']
            )
            user.save()
            telegram_profile = TelegramProfile.objects.create(
                user=user,
                telegram_id=serializer.validated_data['telegram_id'],
                username=serializer.validated_data['username']
            )
            session['telegram_id'] = str(telegram_profile.telegram_id)
            session.save()
            session.modified = True

            return Response(
                status=status.HTTP_201_CREATED
            )

        # if user exists
        telegram_profile = TelegramProfile.objects.get(
            telegram_id=serializer.validated_data['telegram_id']
        )
        session['telegram_id'] = str(telegram_profile.telegram_id)
        session.save()
        session.modified = True

        return Response(
            status=status.HTTP_200_OK
        )


class AuthTelegramCheckView(APIView):
    permission_classes = [AuthTelegramCheckPermission]

    def get(self, request):
        telegram_id = request.session.get('telegram_id')

        if telegram_id is None:
            logging.error('Session doesn\'t exist or telegram_id in session does not exist')
            return Response({'error': 'User not authenticated'}, status=403)

        telegram_profile = TelegramProfile.objects.get(telegram_id=telegram_id)
        login(request, telegram_profile.user)

        del request.session['telegram_id']
        request.session.modified = True

        next_url = request.GET.get('next', 'dashboards:design')
        resolved_url = resolve_url(next_url)

        return Response(
            headers={
                'HX-Redirect': resolved_url
            },
            status=status.HTTP_200_OK
        )


class PostCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostCreateSerializer
    permission_classes = [BotHandlerTokenPermission]

    def perform_create(self, serializer):
        post = serializer.save()
        post.title = f'Пост №{post.id}'
        post.save()


class PostPurchaseViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = PostPurchaseSerializer
    permission_classes = [BotHandlerTokenPermission]

    def get_queryset(self):
        telegram_profile = get_object_or_404(
            TelegramProfile.objects.select_related('user'),
            telegram_id=self.request.headers.get('telegram-id')
        )

        return Post.objects.filter(
            # Owner's posts and purchased posts
            Q(user=telegram_profile.user) | Q(post_purchases__user=telegram_profile.user),
            is_active=True
        ).distinct().prefetch_related('post_purchases')


class LeadViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = LeadSerializer
    permission_classes = [BotHandlerTokenPermission]

    def perform_create(self, serializer):
        return serializer.save(author=serializer.validated_data['post'].user)
