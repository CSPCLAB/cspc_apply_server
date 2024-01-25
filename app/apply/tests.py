from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class GetRecruitSessionTest(APITestCase):
    def test_get_recruit_session(self):
        url = reverse('get_recuit_session')  # 이제 이 이름을 사용할 수 있습니다.
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 추가적인 응답 데이터 검증을 여기에 추가할 수 있습니다.


class ResumeAPITest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_get_resume(self):
        url = reverse('resume_api')  # 이 부분은 실제 뷰의 URL에 맞게 수정해야 합니다.
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
