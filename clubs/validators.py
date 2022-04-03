from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import timedelta



def validate_date(deadline):
    if deadline < date.today():
        raise ValidationError(
        _('%(deadline)s is not a valid date'),
        params={'deadline': deadline},
        )
