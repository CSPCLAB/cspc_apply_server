from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import Applicant, LabMaster
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apply.models import Recruitment, RecruitProcess
from .factories import UserFactory
from datetime import datetime

User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        super().setUp()
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

        self.check_applicant_url = reverse("check_applicant")
        self.get_master_info_url = reverse("get_master_info")

        # UserFactory를 사용하여 테스트용 사용자 생성
        # 동적으로 student_id 생성
        unique_suffix = datetime.now().strftime("%Y%m%d%H%M%S%f")
        dynamic_student_id = f"student_{unique_suffix}"

        # UserFactory를 사용하여 테스트용 사용자 생성 (동적 student_id 사용)
        self.user = UserFactory(student_id=dynamic_student_id)

    def test_existing_applicant_login_success(self):
        """
        기존 지원자가 로그인에 실패한 경우, 상태 코드 500을 반환하는지 확인합니다.
        """
        Applicant.objects.create_user(
            student_id="20240000", password="existingpassword"
        )
        data = {"student_id": "20240000", "password": "notexistingpassword"}
        response = self.client.post(self.check_applicant_url, data, format="json")
        self.assertEqual(response.status_code, 500)

    def test_new_applicant_with_apply_status(self):
        """
        신규 지원자가 'APPLY' 상태에서 지원할 때, 상태 코드 200을 반환하고 지원자의 ID를 반환하는지 확인합니다.
        """
        data = {"student_id": "20241111", "password": "itsnewpassword"}
        response = self.client.post(self.check_applicant_url, data, format="json")

        self.assertEqual(response.status_code, 200)
        # 반환된 ID가 새로 생성된 Applicant 객체의 ID와 일치하는지 확인
        created_applicant = Applicant.objects.get(student_id="20241111")
        self.assertEqual(response.data, created_applicant.id)

    def test_new_applicant_not_apply_status(self):
        """
        신규 지원자가 'APPLY' 상태가 아닐 때 지원하려고 하면, 상태 코드 405를 반환하는지 확인합니다.
        """
        # Recruitment 상태를 변경합니다.
        self.recruitment.process = RecruitProcess.CLOSE
        self.recruitment.save()

        data = {"student_id": "20242222", "password": "notapply"}
        response = self.client.post(self.check_applicant_url, data, format="json")
        self.assertEqual(response.status_code, 405)

    def test_applicant_exists_return_status_201(self):
        """
        사용자가 이미 존재하는 경우(기존 지원자인 경우), 상태 코드 201을 반환하고 사용자의 ID를 반환하는지 확인합니다.
        """
        # 미리 사용자 생성
        created_user = Applicant.objects.create_user(
            student_id="20243333", password="correcting"
        )
        data = {"student_id": "20243333", "password": "correcting"}
        response = self.client.post(self.check_applicant_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        # 반환된 데이터가 사용자의 ID인지 확인
        self.assertEqual(response.data, created_user.id)

    def test_missing_student_id_or_password_return_status_404(self):
        """
        이름과 패스워드를 추출하지 못한 경우, 상태 코드 404를 반환하는지 확인합니다.
        """
        data = {}  # student_id와 password를 전달하지 않음
        response = self.client.post(self.check_applicant_url, data, format="json")
        self.assertEqual(response.status_code, 404)
