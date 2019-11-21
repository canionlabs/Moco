from django.shortcuts import render
from django.views.generic import View

from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class SendMessage(View):

    ACCOUNT_SID = settings.ACCOUNT_SID
    TOKEN_TW = settings.AUTH_TOKEN
    FROM = settings.FROM_


    def send_message(to, message):
        client = Client(self.ACCOUNT_SID, self.TOKEN_TW)

        try:
            message = client.messages.create(
                to = to,
                from_ = self.FROM_,
                body = message
            )
        except TwilioRestException as e:
            print(e)

    def get(self, request, *args, **kwargs):
        data = request.GET

        self.send_message(to=data["token"], message=data["message"])
