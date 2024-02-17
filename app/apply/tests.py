from datetime import timedelta
import datetime
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import Applicant
from django.utils import timezone
from rest_framework.test import APIClient
from apply.models import (
    InterviewTime,
    RecruitProcess,
    Recruitment,
    Resume,
    InterviewPlace,
)


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

        # InterviewPlace 인스턴스 생성
        interview_place = InterviewPlace.objects.create(place="새로운 면접 장소")

        self.resume = Resume.objects.create(
            applicant=self.user,
            phone="01011112222",
            name="홍길동",
            semester=2,
            introduce="hi",
            motivate="cspc is the best",
            to_do="MT",
            etc="etc",
            interview_requirement="nothing",
            interview_place=interview_place,
            updated_at=(timezone.now() + timedelta(days=1)).isoformat(),
            fixed_interview_time=(timezone.now() + timedelta(days=30)).isoformat(),
            created_at=timezone.now().isoformat(),
            is_pass_document=True,
            is_pass_final=False,
        )
        # interview_time_choice 필드에 대한 관계는 따로 설정
        # interview_time_choices = InterviewTime.objects.filter(id__in=[0, 3])
        interview_time_choices_ids = list(
            InterviewTime.objects.filter(id__in=[2, 4]).values_list("id", flat=True)
        )
        self.resume.interview_time_choice.set(interview_time_choices_ids)

        self.get_recuit_session_url = reverse("get_recuit_session")
        self.get_interview_time_list_url = reverse("get_interview_time_list")
        self.get_result_url = reverse("get_result")
        self.resume_api_url = reverse("resume_api")
        self.check_applicant_url = reverse("check_applicant")

        # 로그인
        self.client.force_authenticate(user=self.user)

    def test_get_resume(self):
        """GET 요청으로 Resume 정보를 조회할 수 있는지 테스트하고 field 내용을 가지고 있는지 확인합니다."""
        response = self.client.get(self.resume_api_url)
        self.assertEqual(response.status_code, 200)

        self.assertIn("name", response.data)
        self.assertIn("semester", response.data)
        self.assertIn("phone", response.data)
        self.assertIn("interview_time_choice", response.data)

    def test_create_resume(self):
        """POST 요청으로 새로운 Resume 정보를 생성할 수 있는지 테스트하고 field 내용을 가지고 있는지 확인합니다."""
        interview_place2 = InterviewPlace.objects.create(place="알구일사")

        # 올바른 InterviewTime ID 목록 확보
        interview_time_ids = list(InterviewTime.objects.values_list("id", flat=True))

        # 기존 Resume 데이터 삭제 후 user 정보 재사용
        Resume.objects.filter(applicant=self.user).delete()

        data = {
            "applicant": self.user.id,
            "phone": "01011112222",
            "name": "홍길동",
            "semester": 2,
            "introduce": "hi",
            "motivate": "cspc is the best",
            "to_do": "MT",
            "etc": "etc",
            "interview_time_choice": interview_time_ids,
            "fixed_interview_time": (timezone.now() + timedelta(days=30)).isoformat(),
            "interview_requirement": "nothing",
            "interview_place": interview_place2.id,
            "created_at": timezone.now().isoformat(),
            "updated_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "is_pass_document": True,
            "is_pass_final": True,
        }
        response = self.client.post(self.resume_api_url, data, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertIn("name", response.data)
        self.assertIn("semester", response.data)
        self.assertIn("phone", response.data)
        self.assertIn("interview_time_choice", response.data)

    def test_patch_resume(self):
        """PATCH 요청으로 기존 Resume 정보를 부분적으로 수정할 수 있는지 테스트합니다."""
        patch_data = {
            "introduce": "안녕하세요",
            "motivate": "고기 먹고 싶어요",
            "to_do": "회식하고 싶어요",
            "name": "김서강",
        }  # 수정할 데이터
        response = self.client.patch(self.resume_api_url, patch_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("introduce", response.data)
        self.assertIn("motivate", response.data)
        self.assertIn("to_do", response.data)
        self.assertIn("name", response.data)
        self.assertIn("applicant", response.data)

    def test_get_result_authenticated(self):
        """
        인증받은 결과이면 200을 반환하고 나머지 field 값들을 가지는지 확인합니다.
        """
        # 로그인한 사용자 정보 확인
        response = self.client.get(self.get_result_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.data)
        self.assertIn("interview_place", response.data)

    def tearDown(self):
        # 인증 해제
        self.client.force_authenticate(user=None)

    def test_get_result_unauthenticated(self):
        """
        인증받지 못한 결과이면 401을 반환하는지 확인합니다.
        """
        # 명시적으로 인증 해제
        self.client.force_authenticate(user=None)

        response = self.client.get(self.get_result_url)
        self.assertEqual(response.status_code, 401)

    def test_get_recruit_session_with_existing_session(self):
        """
        존재하는 채용 세션 데이터가 있으면 200을 반환하고 나머지 field 값들을 가지는지 확인합니다.
        """
        response = self.client.get(self.get_recuit_session_url)
        self.assertEqual(response.status_code, 200)

        self.assertIn("year", response.data)
        self.assertIn("term", response.data)
        self.assertIn("start_time", response.data)
        self.assertIn("document_deadline", response.data)
        self.assertIn("announce_middle_time", response.data)
        self.assertIn("interview_start_time", response.data)
        self.assertIn("interview_end_time", response.data)
        self.assertIn("announce_final_time", response.data)
        self.assertIn("process", response.data)

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

        self.assertIn("year", response.data)
        self.assertIn("term", response.data)
        self.assertIn("start_time", response.data)
        self.assertIn("document_deadline", response.data)
        self.assertIn("announce_middle_time", response.data)
        self.assertIn("interview_start_time", response.data)
        self.assertIn("interview_end_time", response.data)
        self.assertIn("announce_final_time", response.data)
        self.assertIn("process", response.data)

    def test_get_interview_time_list_with_existing_data(self):
        """
        존재하는 인터뷰 시간 데이터가 있으면 200 반환하는지, 인터뷰시간이 한개 이상 존재하는지, time을 가지는지 확인합니다.
        """
        response = self.client.get(self.get_interview_time_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

        for item in response.data:
            self.assertIn("time", item)
