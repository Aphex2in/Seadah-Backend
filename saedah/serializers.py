from rest_framework import serializers
from .models import User,Deal

class UserSerializer(serializers.ModelSerializer):
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
    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
    
class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['id','posted_by','location','title','description','expiry_date','tags','upvotes','downvotes','price','voucher','latitude','longitude']
    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        return {"latitude": obj.latitude, "longitude": obj.longitude}

    def set_location(self, validated_data, instance):
        # Extract the 'location' data from the POST request and set it in 'latitude' and 'longitude' fields.
        location_data = validated_data.get('location')
        if location_data:
            latitude = location_data.get('latitude')
            longitude = location_data.get('longitude')
            if latitude is not None:
                instance.latitude = latitude
            if longitude is not None:
                instance.longitude = longitude
        return instance