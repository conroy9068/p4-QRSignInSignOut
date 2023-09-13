from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    qr_code = models.FileField(upload_to='qr_codes/', null=True, blank=True)


    def __str__(self):
        return self.name
    


class SignInOutRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    sign_in_time = models.DateTimeField()
    sign_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.location.name}"

