from datetime import timedelta
import datetime
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import Applicant
from django.utils import timezone
from rest_framework.test import APIClient
from apply.models import InterviewTime, RecruitProcess, Recruitment, Resume


class GetResultAPITest(TestCase):
    def setUp(self):
        # 'APPLY' 상태의 Recruitment 인스턴스 생성
        # start_time, document_deadline 등 필요한 필드 값 설정
        start_time = timezone.now().date() - timedelta(days=1)  # 어제 시작
        document_deadline = timezone.now().date() + timedelta(days=1)  # 내일 마감
        announce_middle_time = timezone.now() + timedelta(days=2)
        interview_start_time = timezone.now().date() + timedelta(days=3)
        interview_end_time = timezone.now().date() + timedelta(days=4)
        announce_final_time = timezone.now() + timedelta(days=5)

        self.recruitment = Recruitment.objects.create(
            year=2023,
            term="Spring",
            start_time=start_time,
            document_deadline=document_deadline,
            announce_middle_time=announce_middle_time,
            interview_start_time=interview_start_time,
            interview_end_time=interview_end_time,
            announce_final_time=announce_final_time,
            process=RecruitProcess.APPLY,
        )
        self.client = APIClient()
        self.user = Applicant.objects.create_user(
            student_id="testuser", password="tmppassword"
        )

        self.interview = InterviewTime.objects.create(
            time="2024-02-20 10:00:00", is_fixed=True
        )
        # self.resume = Resume.objects.create(
        #     applicant=self.user,
        #     phone="01011112222",
        #     name="홍길동",
        #     semester=2,
        #     introduce="hi",
        #     motivate="hoho",
        #     to_do="todo",
        #     etc="etcc",
        # )  # 적절한 필드값 전달해야 함

        self.get_recuit_session_url = reverse("get_recuit_session")
        self.get_interview_time_list_url = reverse("get_interview_time_list")
        self.get_result_url = reverse("get_result")
        self.resume_api_url = reverse("resume_api")

    def test_get_result_authenticated(self):
        """
        인증받은 결과이면 200을 반환하는지 확인합니다.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.get_result_url)
        self.assertEqual(response.status_code, 200)

    def test_get_result_unauthenticated(self):
        """
        인증받지 못한 결과이면 401을 반환하는지 확인합니다.
        """
        response = self.client.get(self.get_result_url)
        self.assertEqual(response.status_code, 401)

    def test_get_recruit_session_with_existing_session(self):
        """
        존재하는 채용 세션 데이터가 있으면 200 반환하는지 확인합니다.
        """
        response = self.client.get(self.get_recuit_session_url)
        self.assertEqual(response.status_code, 200)

        # 응답 데이터에는 채용 세션 정보가 포함되어야 합니다.
        self.assertIn("year", response.data)
        self.assertIn("term", response.data)

    def test_get_recruit_session_without_existing_session(self):
        """
        존재하지 않는 채용 세션 데이터면 404 반환하는지 확인합니다.
        """
        response = self.client.get(self.get_recuit_session_url)
        self.assertEqual(response.status_code, 404)

    @patch("apply.views.get_object_or_404")
    @patch("apply.views.RecruitSerializer")
    def test_get_recruit_session_check_process_called(
        self, mock_serializer, mock_get_object_or_404
    ):
        # Mock 객체를 설정합니다.
        mock_recruitment = mock_get_object_or_404.return_value
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = {
            "year": 2024,
            "term": "Spring",
            "start_time": timezone.now().date() - timedelta(days=1),
            "document_deadline": timezone.now().date() + timedelta(days=1),
            "announce_middle_time": timezone.now() + timedelta(days=2),
            "interview_start_time": timezone.now().date() + timedelta(days=3),
            "interview_end_time": timezone.now().date() + timedelta(days=4),
            "announce_final_time": timezone.now() + timedelta(days=5),
            "process": RecruitProcess.CLOSE,
        }
        response = self.client.get(self.get_recuit_session_url)

        # RecruitSerializer와 get_object_or_404가 올바르게 호출되었는지 확인합니다.
        mock_get_object_or_404.assert_called_once_with(Recruitment)
        mock_recruitment.check_process.assert_called_once()
        self.assertEqual(response.status_code, 200)

        # 응답 데이터에는 채용 세션 정보가 포함되어야 합니다.
        self.assertIn("year", response.data)
        self.assertIn("term", response.data)

    def test_get_interview_time_list_without_existing_data(self):
        """
        존재하는 인터뷰 시간 데이터가 없을 때 200 반환하는지 확인합니다.
        """
        response = self.client.get(self.get_interview_time_list_url)
        self.assertEqual(response.status_code, 200)

        # 응답 데이터가 비어 있어야 합니다.
        self.assertEqual(len(response.data), 0)

    def test_get_interview_time_list_with_existing_data(self):
        """
        존재하는 인터뷰 시간 데이터가 있으면 200 반환하는지 확인합니다.
        """
        response = self.client.get(self.get_interview_time_list_url)
        self.assertEqual(response.status_code, 200)

    # Resume 관련해서는 하다가 "interview_time_choice"와 같은
    # 여러개 복수 선택 부분을 어떻게 테스트 해야 할지 모르겠어서 일단 보류했습니다...
