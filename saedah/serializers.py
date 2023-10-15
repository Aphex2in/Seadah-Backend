from rest_framework import serializers
from .models import DealPhotos, User,Deal

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
    
class DealPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealPhotos
        fields = ['id', 'image']

class DealSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ['id', 'posted_by', 'title', 'description', 'expiry_date', 'tags', 'upvotes', 'downvotes', 'price', 'voucher', 'latitude', 'longitude', 'photos']

    def get_upvotes(self, obj):
        return obj.upvotes.count()

    def get_downvotes(self, obj):
        return obj.downvotes.count()

    def get_photos(self, obj):
        photos = DealPhotos.objects.filter(deal=obj)
        return [photo.photo.url for photo in photos]
    
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