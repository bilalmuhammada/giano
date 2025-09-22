from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    token = models.CharField(max_length=64, unique=True)
    numeric_code = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Session {self.token} - code={self.numeric_code} - verified={self.verified}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    signin_at = models.DateTimeField(null=True, blank=True)
    signout_at = models.DateTimeField(null=True, blank=True)
    device = models.CharField(max_length=100, blank=True)
    scan_session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} @ {self.timestamp}"
