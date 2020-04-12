from datetime import timedelta

import pytest
from django.utils import timezone
from django.test import override_settings
from freezegun import freeze_time

from model_bakery import baker

from messages_tw.models import Message


DEFAULT_TEST_DELAY = 1


@override_settings(MESSAGE_DELAY_IN_HOURS=DEFAULT_TEST_DELAY)
@pytest.mark.django_db
def test_with_repeatedly_recently_messages():
    created_at = timezone.now() - timedelta(hours=DEFAULT_TEST_DELAY / 2)
    with freeze_time(created_at):
        message = baker.make(Message, created_at=created_at)

    message_qs = Message.objects.repeatedly_recently(message)

    assert message_qs.exists()


@override_settings(MESSAGE_DELAY_IN_HOURS=DEFAULT_TEST_DELAY)
@pytest.mark.django_db
def test_without_repeatedly_recently_messages():
    created_at = timezone.now() - timedelta(hours=DEFAULT_TEST_DELAY * 2)
    with freeze_time(created_at):
        message = baker.make(Message, created_at=created_at, _quantity=3)[0]

    message_qs = Message.objects.repeatedly_recently(message)

    assert not message_qs.exists()
