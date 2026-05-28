from django.db import models
from django.utils.timezone import now


class OTPTransaction(models.Model):
    txn_id = models.CharField(max_length=120, unique=True)
    otp = models.CharField(max_length=6)
    client_id = models.CharField(max_length=120)

    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"{self.txn_id} ({'verified' if self.is_verified else 'pending'})"