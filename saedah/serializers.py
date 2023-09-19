from rest_framework import serializers
from .models import User

class SaedahSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','fullname','username','email','password','role']