from django.urls import path
from .views import SendMessage

urlpatterns = [
    path('message/', SendMessage.as_view(), name="send_tw"),
]
