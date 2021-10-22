import pytest
from django.urls import reverse
from faker import Factory
from rest_framework import status

from tests.helper_requests import request_helper

user_fake = Factory.create(locale='ko_KR')


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_signup(user_context, rf):
    data = {
        'username': user_fake.uuid4().split('-')[0],
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

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == data['username']
    assert response.data['name'] == data['name']
    assert response.data['phone'] == data['phone']
    assert response.data['email'] == data['email']
    assert response.data['role']
    assert response.data['created_at']
    assert response.data['updated_at']
