from django.urls import path
from milestone2.notify_update.views.notify_view import NotifyCareContextUpdateView

urlpatterns = [
    path('notify/', NotifyCareContextUpdateView.as_view(), name='notify-update'),
]