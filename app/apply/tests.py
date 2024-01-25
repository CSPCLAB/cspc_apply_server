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
    def test_recruitment_process_states(self):
        dates_to_test = {
            RecruitProcess.CLOSE: timezone.make_aware(datetime(2020, 1, 1)),
            RecruitProcess.APPLY: timezone.make_aware(datetime(2020, 1, 10)),
            RecruitProcess.MIDDLE: timezone.make_aware(datetime(2020, 1, 15)),
            RecruitProcess.FINAL: timezone.make_aware(datetime(2020, 1, 20)),
        }

        for state, test_date in dates_to_test.items():
            with self.subTest(state=state):
                with patch('django.utils.timezone.now', return_value=test_date):
                    recruitment = self.create_recruitment(state, save=False)
                    recruitment.check_process()
                    self.assertEqual(recruitment.process, state)