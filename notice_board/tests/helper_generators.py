import factory
from faker import Factory

from apps.users.models import User
from apps.post.models import Post

user_fake = Factory.create(locale="ko_KR")


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda x: user_fake.uuid4().split('-')[0])
    name = factory.Sequence(lambda x: user_fake.name())
    email = factory.Sequence(lambda x: user_fake.email())
    phone = factory.Sequence(lambda x: user_fake.phone_number().replace('-', ''))
    role = User.GENERAL
    password = 'Abcde11!'

    class Meta:
        model = User


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda x: user_fake.sentence()[:49])
    content = factory.Sequence(lambda x: " ".join(user_fake.sentences()))

    class Meta:
        model = Post
