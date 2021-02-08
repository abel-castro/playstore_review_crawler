from django.utils.timezone import make_aware


def make_aware_if_is_not_none(unaware_datetime):
    if not unaware_datetime:
        return
    return make_aware(unaware_datetime)
