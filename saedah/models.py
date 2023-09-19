from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=24)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=24)
    #roles
    US = "User"
    MD = "Moderator"
    AD = "Admin"
    DW = "awd"
    ROLE_CHOICES = (
        (US, "User"),
        (MD, "Moderator"),
        (AD, "Admin")
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default=US)

    def __str__(self):
        return str(self.id)