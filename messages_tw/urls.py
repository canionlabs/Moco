from django.urls import path
from .views import SendWhatsappMessage, SendSMSMessage


urlpatterns = [
    path('message/whatsapp/', SendWhatsappMessage.as_view(), name="send_whatsapp"),
    path('message/sms/', SendSMSMessage.as_view(), name="send_sms"),
]
