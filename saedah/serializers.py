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
        fields = ['id','posted_by','title','description','expiry_date','tags','upvotes','downvotes','price','voucher','latitude','longitude']
    
class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'username', 'role', 'followers', 'followings', 'avatar']

    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_followings(self, obj):
        return obj.following.count()