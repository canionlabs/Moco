from django.views.generic import View

from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class SendMessage(View):

    ACCOUNT_SID = settings.ACCOUNT_SID
    TOKEN_TW = settings.AUTH_TOKEN
    FROM = settings.FROM_


    def send_message(self, to, message):
        client = Client(self.ACCOUNT_SID, self.TOKEN_TW)

        try:
            message = client.messages.create(
                to='+55'+to,
                from_=self.FROM,
                body=message,
            )

            print(message.sid)

        except TwilioRestException as e:
            raise


    def get(self, request, *args, **kwargs):
        data = request.GET

        self.send_message(to=data['to'], message=data['message'])
