import json

import pytest
from django.urls import reverse
from faker import Factory
from oauth2_provider.models import AccessToken, RefreshToken
from rest_framework import status

from tests.helper_requests import request_helper, get_oauth2_client

user_fake = Factory.create(locale='ko_KR')


@pytest.mark.urls(urls='oauth2_provider.urls')
@pytest.mark.django_db()
def test_login(user_context, rf):
    user = user_context['user_data'].create()
    user.set_password('Abcde11!')
    user.save()
    data = f'grant_type=password&username={user.username}&password=Abcde11!&scope=read write'
    url = reverse('token')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        token=get_oauth2_client(user),
        data=data,
        basic=True,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_200_OK
    response = json.loads(response.content)
    assert response['access_token']
    assert response['expires_in']
    assert response['token_type']
    assert response['scope']
    assert response['refresh_token']
    assert AccessToken.objects.filter(token=response['access_token']).exists()
    assert RefreshToken.objects.filter(token=response['refresh_token']).exists()
