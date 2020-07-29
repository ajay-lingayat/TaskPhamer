from django.db import models

class otp_verification(models.Model):
    otp = models.IntegerField()
    email = models.CharField(max_length=50)
