# user/factories.py

import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # 지원자를 위한 필드
    student_id = factory.Sequence(lambda n: f"202415{n:02d}")
    password = factory.PostGenerationMethodCall("set_password", "testpassword123")
