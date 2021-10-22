import pytest
from django.urls import reverse
from faker import Factory
from rest_framework import status

from apps.post.models import Post, DeletePost
from tests.helper_requests import request_helper, get_oauth2_token

user_fake = Factory.create(locale='ko_KR')


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_create(user_context, rf):
    user = user_context['user_data'].create()
    data = {
        'title': user_fake.sentence()[:49],
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

    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.filter(id=response.data['id']).exists()
    assert response.data['created_at']
    assert response.data['updated_at']
    assert response.data['title'] == data['title'].rstrip()
    assert response.data['content'] == data['content']


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_list_token(user_context, rf):
    user = user_context['user_data'].create()
    posts = user_context['post_data'].create_batch(writer=user, size=50)
    url = reverse('posts-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='get',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == len(posts)
    assert len(response.data['results']) == 25


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_list(user_context, rf):
    user = user_context['user_data'].create()
    posts = user_context['post_data'].create_batch(writer=user, size=50)
    url = reverse('posts-list')
    response = request_helper(
        rf=rf,
        url=url,
        method='get',
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == len(posts)
    assert len(response.data['results']) == 25


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_detail_token(user_context, rf):
    user = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user)
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='get',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['created_at']
    assert response.data['updated_at']
    assert response.data['id'] == post.id
    assert response.data['title'] == post.title
    assert response.data['content'] == post.content


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_detail(user_context, rf):
    user = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user)
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='get',
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['created_at']
    assert response.data['updated_at']
    assert response.data['id'] == post.id
    assert response.data['title'] == post.title
    assert response.data['content'] == post.content


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_update(user_context, rf):
    user = user_context['user_data'].create()
    post = user_context['post_data'].create(writer=user)
    data = {
        'title': user_fake.sentence()[:49],
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

    assert response.status_code == status.HTTP_200_OK
    assert Post.objects.filter(id=post.id).exists()
    assert response.data['created_at']
    assert response.data['updated_at']
    assert response.data['id'] == post.id
    assert response.data['title'] == data['title'].rstrip()
    assert response.data['content'] == data['content']


@pytest.mark.urls(urls='notice_board.urls')
@pytest.mark.django_db()
def test_post_delete(user_context, rf):
    user = user_context['user_data'].create()
    user_context['post_data'].create(writer=user)
    user_context['post_data'].create(writer=user)
    user_context['post_data'].create(writer=user)
    post = user_context['post_data'].create(writer=user)
    url = reverse('posts-detail', kwargs={'pk': post.id})
    response = request_helper(
        rf=rf,
        url=url,
        method='delete',
        token=get_oauth2_token(user)['access_token'],
        user=user,
        **user_context['headers']
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Post.objects.filter(id=post.id).exists()
    assert DeletePost.objects.filter(id=post.id).exists()
