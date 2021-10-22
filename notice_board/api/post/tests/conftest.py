import pytest
from faker import Factory

from tests.helper_generators import UserFactory, PostFactory
from tests.helper_requests import WEB_HEADERS

user_fake = Factory.create(locale="ko_KR")


@pytest.fixture(scope='function')
def user_context():
    return {
        'headers': WEB_HEADERS,
        'user_data': UserFactory,
        'post_data': PostFactory
    }