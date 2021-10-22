import pytest
from django.urls import reverse
from faker import Factory
from rest_framework import status

from tests.helper_requests import request_helper, get_oauth2_client

user_fake = Factory.create(locale='ko_KR')


@pytest.mark.urls(urls='oauth2_provider.urls')
@pytest.mark.django_db()
def test_fail_login_username(user_context, rf):
    user = user_context['user_data'].create()
    user.set_password('Abcde11!')
    user.save()
    data = f'grant_type=password&username=&password=Abcde11!&scope=read write'
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

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='oauth2_provider.urls')
@pytest.mark.django_db()
def test_fail_login_password(user_context, rf):
    user = user_context['user_data'].create()
    user.set_password('Abcde11!')
    user.save()
    data = f'grant_type=password&username={user.username}&password=&scope=read write'
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

    assert response.status_code == status.HTTP_400_BAD_REQUEST
