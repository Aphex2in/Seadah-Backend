from rest_framework import serializers
from .models import Comments, DealPhotos, User,Deal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','fullname','username','email','password','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.get('role', User.US)

        user = User(
            fullname=validated_data['fullname'],
            username=validated_data['username'],
            email=validated_data['email'],
            role=role
        )
        if role == User.AD:
            user.is_staff = True
            user.is_superuser = True
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

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='posted_by.username')
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['Deal_id', 'posted_by', 'content', 'created_at', 'username', 'avatar']

    def get_avatar(self, obj):
        avatar_url = obj.posted_by.avatar.url if obj.posted_by.avatar else None
        return avatar_url

class DealSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ['id', 'posted_by', 'title', 'description', 'expiry_date', 'isLiked', 'tags', 'upvotes', 'downvotes', 'price', 'voucher', 'latitude', 'longitude', 'photos', 'comments']

    def get_upvotes(self, obj):
        return obj.upvotes.count()

    def get_downvotes(self, obj):
        return obj.downvotes.count()

    def get_photos(self, obj):
        photos = DealPhotos.objects.filter(deal=obj)
        return [photo.photo.url for photo in photos]
    
    def get_comments(self, obj):
        comments = Comments.objects.filter(Deal_id=obj.id)
        comment_serializer = CommentSerializer(comments, many=True)
        return {'comments': comment_serializer.data}
    
class LikeSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    class Meta:
        model = Deal
        fields = ['id', 'posted_by', 'title', 'description' ,'photos']

    def get_photos(self, obj):
        photos = DealPhotos.objects.filter(deal=obj)
        return [photo.photo.url for photo in photos]

class UserCustomSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['fullname', 'username', 'role', 'followers', 'followings', 'avatar', 'comments', 'likes']

    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_followings(self, obj):
        return obj.following.count()
    
    def get_comments(self, obj):
        comments = Comments.objects.filter(posted_by=obj)
        comment_serializer = CommentSerializer(comments, many=True)
        return {'comments': comment_serializer.data}
    
    def get_likes(self, obj):
        likes = Deal.objects.filter(likes=obj)
        like_serializer = LikeSerializer(likes, many=True)
        return {'likes': like_serializer.data}