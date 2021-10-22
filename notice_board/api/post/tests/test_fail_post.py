import pytest
from django.urls import reverse
from faker import Factory
from rest_framework import status

from apps.post.models import Post
from tests.helper_requests import request_helper, get_oauth2_token

user_fake = Factory.create(locale='ko_KR')


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_create_title(user_context, rf):
    user = user_context['user_data'].create()
    data = {
        'title': '',
        'content': " ".join(user_fake.sentences()),
        'writer': user.id
    }
    url = reverse('posts-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_create_content(user_context, rf):
    user = user_context['user_data'].create()
    data = {
        'title': user_fake.sentence()[:49],
        'content': "",
        'writer': user.id
    }
    url = reverse('posts-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_create_writer(user_context, rf):
    user = user_context['user_data'].create()
    data = {
        'title': user_fake.sentence()[:49],
        'content': " ".join(user_fake.sentences()),
        'writer': ''
    }
    url = reverse('posts-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='post',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_update_other_user(user_context, rf):
    user1 = user_context['user_data'].create()
    user2 = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user1)
    data = {
        'title': user_fake.sentence()[:49],
        'content': " ".join(user_fake.sentences()),
    }
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='patch',
        token=get_oauth2_token(user2)['access_token'],
        user=user2,
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "Can't approach other user post"


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_update_title(user_context, rf):
    user = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user)
    data = {
        'title': '',
        'content': " ".join(user_fake.sentences()),
    }
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='patch',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_update_content(user_context, rf):
    user = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user)
    data = {
        'title': user_fake.sentence()[:49],
        'content': "",
    }
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='patch',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        data=data,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_fail_post_delete_other_user(user_context, rf):
    user1 = user_context['user_data'].create()
    user2 = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user1)
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='delete',
        token=get_oauth2_token(user2)['access_token'],
        user=user2,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Post.objects.filter(id=post.id).exists()
    assert response.data[0] == "Can't approach other user post"
