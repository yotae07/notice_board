import pytest
from django.urls import reverse
from faker import Factory
from rest_framework import status

from tests.helper_requests import request_helper

user_fake = Factory.create(locale='ko_KR')


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_signup_username(user_context, rf):
    data = {
        'username': '가나다라마바사',
        'name': user_fake.name(),
        'email': user_fake.email(),
        'phone': user_fake.phone_number().replace('-', ''),
        'role': 'general',
        'password': 'Abcde11!'
    }
    url = reverse('users-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_signup_name(user_context, rf):
    data = {
        'username': user_fake.uuid4().split('-')[0],
        'name': 'abcdefg',
        'email': user_fake.email(),
        'phone': user_fake.phone_number().replace('-', ''),
        'role': 'general',
        'password': 'Abcde11!'
    }
    url = reverse('users-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_signup_email(user_context, rf):
    data = {
        'username': user_fake.uuid4().split('-')[0],
        'name': user_fake.name(),
        'email': 'aa.com',
        'phone': user_fake.phone_number().replace('-', ''),
        'role': 'general',
        'password': 'Abcde11!'
    }
    url = reverse('users-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_signup_phone(user_context, rf):
    data = {
        'username': user_fake.uuid4().split('-')[0],
        'name': user_fake.name(),
        'email': user_fake.email(),
        'phone': 'phonephone',
        'role': 'general',
        'password': 'Abcde11!'
    }
    url = reverse('users-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
