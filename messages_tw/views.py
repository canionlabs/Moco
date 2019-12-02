from django.views.generic import View
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from twilio.rest import Client


class BaseMessageSender(APIView):

    permission_classes = [IsAuthenticated]

    ACCOUNT_SID = settings.ACCOUNT_SID
    TOKEN_TW = settings.AUTH_TOKEN
    FROM = settings.FROM_

    #API Twilio connection
    def client_message(self, to, from_, message):
        client = Client(self.ACCOUNT_SID, self.TOKEN_TW)
        message = client.messages.create(
            to=to,
            from_=from_,
            body=message,
        )

    def send_whatsapp(self, to, message):
        to_whatsapp = 'whatsapp:'+to
        from_ = 'whatsapp:'+ self.FROM

        self.client_message(to_whatsapp, from_, message)

    def send_sms(self, to, message):
        to_sms = to
        from_ = self.FROM

        self.client_message(to_sms, from_, message)


class SendWhatsappMessage(BaseMessageSender):

    def post(self, request, *args, **kwargs):
        to = request.data["to"]
        message = request.data["message"]

        self.send_whatsapp(to=to, message=message)


class SendSMSMessage(BaseMessageSender):

    def post(self, request, *args, **kwargs):
        to = request.data["to"]
        message = request.data["message"]

        self.send_sms(to=to, message=message)
