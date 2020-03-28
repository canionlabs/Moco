from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class MessageManager(models.Manager):
    def repeatedly_recently(self, message: "Message"):
        delay = timedelta(hours=settings.MESSAGE_DELAY_IN_HOURS)
        queryset = self.get_queryset()

        if message.pk is not None:
            queryset.exclude(pk=message.pk)

        return queryset.filter(
            number_from=message.number_from,
            number_to=message.number_to,
            content=message.content,
            kind=message.kind,
            has_blocked=False,
            has_error=False,
            created_at__gte=timezone.now() - delay,
        )


class Message(models.Model):
    WHATSAPP = "whatsapp"
    SMS = "sms"

    KIND_CHOICES = (
        (WHATSAPP, "Whatsapp"),
        (SMS, "SMS"),
    )
    number_from = models.CharField(max_length=75)
    number_to = models.CharField(max_length=75)
    content = models.TextField()

    kind = models.CharField(choices=KIND_CHOICES, max_length=15)
    has_blocked = models.BooleanField(default=False)
    has_error = models.BooleanField(default=False)

    creator = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return f"{self.pk}: {self.number_from} - {self.number_to}"
