import logging

from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.shortcuts import resolve_url
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import TelegramProfile, User

from .permissions import AuthTelegramCheckPermission, BotTokenPermission
from .serailizer import TelegramProfileSerializer


class BotManagerAuthView(APIView):
    permission_classes = (BotTokenPermission,)

    def post(self, request, *args, **kwargs):
        '''
        Create or get user and save telegram_id in session.

        Bot manager send django session_id of user
        and his telegram id and username

        Combine telegram and session data to authorize or register a user.
        Save the telegram ID in the session
        '''
        # validate session_id
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
    permission_classes = (AuthTelegramCheckPermission,)

    def get(self, request):
        telegram_id = request.session.get('telegram_id')

        if telegram_id is None:
            logging.error('Session doesn\'t exist or telegram_id in session does not exist')
            return Response({'error': 'User not authenticated'}, status=403)

        telegram_profile = TelegramProfile.objects.get(telegram_id=telegram_id)
        login(request, telegram_profile.user)

        del request.session['telegram_id']
        request.session.modified = True

        next_url = request.GET.get('next', 'posts:index')
        return Response(
            headers={
                'HX-Redirect': resolve_url(next_url)
            },
            status=status.HTTP_302_FOUND
        )
