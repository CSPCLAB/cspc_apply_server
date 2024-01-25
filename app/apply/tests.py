from django.test import TestCase
from django.utils import timezone
from .models import Recruitment, TermType, RecruitProcess
from unittest.mock import patch

class RecruitmentTestCase(TestCase):

    def create_recruitment(self, process_state, save=True):
        """
        Helper method to create a recruitment object with a specific process state.
        """
        now = timezone.now()
        recruitment = Recruitment(
            year=now.year,
            term=TermType.SPRING,
            start_time=now.date() - timezone.timedelta(days=10),
            document_deadline=now.date() + timezone.timedelta(days=10),
            announce_middle_time=now - timezone.timedelta(days=5),
            interview_start_time=now.date() + timezone.timedelta(days=5),
            interview_end_time=now.date() + timezone.timedelta(days=10),
            announce_final_time=now + timezone.timedelta(days=15),
            process=process_state,
        )
        if save:
            recruitment.save()
        return recruitment

    @patch('django.utils.timezone.now')
    def test_recruitment_process_states(self, mock_now):
        """
        Test the get_recuit_session view with different recruitment process states.
        """
        # Simulate different times
        dates_to_test = {
            RecruitProcess.CLOSE: timezone.now() - timezone.timedelta(days=20),
            RecruitProcess.APPLY: timezone.now() - timezone.timedelta(days=5),
            RecruitProcess.MIDDLE: timezone.now(),
            RecruitProcess.FINAL: timezone.now() + timezone.timedelta(days=20),
        }

        for state, mock_date in dates_to_test.items():
            with self.subTest(state=state):
                recruitment = self.create_recruitment(state, save=False)
                mock_now.return_value = mock_date
                recruitment.check_process()
                self.assertEqual(recruitment.process, state)

                # Here you would make a request to your view and assert the response
                response = self.client.get(reverse('get_recuit_session'))
                self.assertEqual(response.status_code, 200)
                # Add more assertions here based on what your view returns
