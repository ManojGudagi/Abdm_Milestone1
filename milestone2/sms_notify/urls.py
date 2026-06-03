from django.urls import path
from milestone2.sms_notify.views.sms_view import SendSmsNotificationView

urlpatterns = [
    path('send/', SendSmsNotificationView.as_view(), name='send-sms'),
]