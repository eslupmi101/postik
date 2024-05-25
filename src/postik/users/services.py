from django.contrib.sessions.models import Session


def is_user_authed_telegram(session_key: str) -> bool:
    '''
    Checked if user is authenticated by telegram manager bot.
    '''
    if not session_key:
        return False

    instance = Session.objects.filter(session_key=session_key)

    if not instance.exists():
        return False

    session = instance.first()
    return session.get_decoded().get('_auth_user_id', False)
