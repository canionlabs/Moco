from django.views.generic import View
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from twilio.base.exceptions import TwilioException

from twilio.rest import Client

from messages_tw.models import Message


class BaseMessageSender(APIView):

    permission_classes = [IsAuthenticated]

    ACCOUNT_SID = settings.ACCOUNT_SID
    TOKEN_TW = settings.AUTH_TOKEN
    FROM = settings.FROM_

    def _client_message(self, message: Message):
        try:
            client = Client(self.ACCOUNT_SID, self.TOKEN_TW)
            client.messages.create(
                to=message.number_to,
                from_=message.number_from,
                body=message.content,
            )
        except TwilioException as e:
            message.has_error = True
            message.save()
            raise e

    def _send_message(self, to: str, message_text: str, kind: str):
        if kind == Message.WHATSAPP:
            message = Message(
                creator=self.request.user,
                number_from=f"whatsapp:{self.FROM}",
                number_to=f"whatsapp:{to}",
                content=message_text,
                kind=Message.WHATSAPP,
            )
        else:
            message = Message.objects.create(
                creator=self.request.user,
                number_from=self.FROM,
                number_to=to,
                content=message_text,
                kind=Message.SMS,
            )

        repeatedly_qs = Message.objects.repeatedly_recently(message)
        if repeatedly_qs.exists():
            message.has_blocked = True
            message.save()
        else:
            self._client_message(message)

        return message

    def _handle_response(self, message: Message):
        if message.has_blocked:
            data = {"error": "A similar message has been sent recently"}
            status_code = status.HTTP_400_BAD_REQUEST
        elif message.has_error:
            data = {"error": "Twilio integration error"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            data = {"message": "Sent successfully"}
            status_code = status.HTTP_200_OK

        return data, status_code


class SendWhatsappMessage(BaseMessageSender):
    def post(self, request, *args, **kwargs):
        to = request.data["to"]
        message = request.data["message"]

        message = self._send_message(to, message, Message.WHATSAPP)
        data, status_code = self._handle_response(message)

        return DRFResponse(data, status=status_code)


class SendSMSMessage(BaseMessageSender):
    def post(self, request, *args, **kwargs):
        to = request.data["to"]
        message = request.data["message"]

        message = self._send_message(to, message, Message.SMS)
        data, status_code = self._handle_response(message)

        return DRFResponse(data, status=status_code)
