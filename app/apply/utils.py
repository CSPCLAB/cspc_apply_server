from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_interview_time(value):
    if value.minute != 0 or value.second != 0:
        raise ValidationError(
            _("시간은 정각이어야 합니다."),
            params={"value": value},
        )
