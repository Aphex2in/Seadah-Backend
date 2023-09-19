from rest_framework import serializers
from .models import User

class SaedahSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','fullname','username','email','password','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            fullname=validated_data['fullname'],
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user