from django.views.generic import View

from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class SendMessage(View):

    ACCOUNT_SID = settings.ACCOUNT_SID
    TOKEN_TW = settings.AUTH_TOKEN
    FROM = settings.FROM_

    #API Twilio connection
    def client_message(self, to, from_, message):
        client = Client(self.ACCOUNT_SID, self.TOKEN_TW)

        try:
            message = client.messages.create(
                to=to,
                from_=from_,
                body=message,
            )

        except TwilioRestException as e:
            raise

    #send message to WHATSAPP
    def send_whatsapp(self, to, message):
        to_whatsapp = 'whatsapp:+55'+to
        from_ = 'whatsapp:'+self.FROM

        self.client_message(to_whatsapp, from_, message)

    #send message to SMS
    def send_sms(self, to, message):
        to_sms = '+55'+to
        from_ = self.FROM

        self.client_message(to_sms, from_, message)

    #get arguments and call the functions send message
    def get(self, request, *args, **kwargs):
        to = request.GET.get('to')
        message = request.GET.get('message')

        self.send_whatsapp(to=to, message=message)
        self.send_sms(to=to, message=message)
