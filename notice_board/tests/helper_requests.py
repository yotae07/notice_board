import base64
import json
from datetime import timedelta
from urllib.parse import urlencode

from django.contrib.sessions.backends.cache import SessionStore
from django.urls import resolve
from django.conf import settings as SETTINGS
from django.utils import timezone
from oauth2_provider.models import AccessToken, RefreshToken, Application, get_application_model
from oauthlib.common import generate_token
from rest_framework.test import force_authenticate

WEB_HEADERS = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Linux; Android 9; SM-G950N Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36 kidsnote/3.2.03 (Build/30430)',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Charset': 'utf-8',
    'HTTP_HOST': SETTINGS.ALLOWED_HOSTS[-1],
    'X-CSRFToken': 'LvfM6TdpbZ8cZQnmqmaZYLuaJF0eKQePl9OszEv6o4e7AjZIQ1t8xukzBa4fr9Bi'
}


def request_helper(rf, url, method, data='', get=None, token=None, user=None, basic=False, **kwargs):
    method = method.lower()
    caller = getattr(rf, method)

    if token:
        if basic:
            kwargs.update({
                'HTTP_AUTHORIZATION': 'Basic {}'.format(token),
            })
            content_type = 'application/x-www-form-urlencoded'
        else:
            kwargs.update({
                'HTTP_AUTHORIZATION': 'Bearer {}'.format(token),
            })
            content_type = 'application/json'
    else:
        if basic:
            content_type = 'application/x-www-form-urlencoded'
        else:
            content_type = 'application/json'

    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data)

    if isinstance(get, dict):
        request_url = '{}?{}'.format(url, urlencode(get))
    else:
        request_url = url

    request = caller(path=request_url, data=data, content_type=content_type, **kwargs)

    if not hasattr(request, 'session'):
        setattr(request, 'session', SessionStore())

    force_authenticate(
        request=request,
        user=user,
        token=AccessToken.objects.filter(token=token).first()
    )

    resolver_match = resolve(url)
    cb, cb_args, cb_kwargs = resolver_match
    request.resolver_match = resolver_match
    response = cb(request, *cb_args, **cb_kwargs)
    return response
