from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=24)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=24)
    #roles
    US = "User"
    MD = "Moderator"
    AD = "Admin"
    ROLE_CHOICES = (
        (US, "User"),
        (MD, "Moderator"),
        (AD, "Admin")
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default=US)

    def __str__(self):
        return str(self.id)
    
class Follower(models.Model):
    followedby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Deal(models.Model):
    id = models.BigAutoField(primary_key=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=124)
    description = models.CharField(max_length=2000)  # You can adjust the max_length as needed.
    latitude = models.FloatField()
    longitude = models.FloatField()
    expiry_date = models.DateField()
    tags = models.CharField(max_length=20)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    voucher = models.CharField(max_length=100)

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    Deal_id = models.ForeignKey(Deal, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=366)