from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class RecruitmentTestCase(APITestCase):
    def test_get_recruit_session(self):

        response = self.client.get(reverse('get_recuit_session'))


        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('key', response.data)
