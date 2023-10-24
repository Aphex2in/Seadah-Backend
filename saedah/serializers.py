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
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    isDeletable = serializers.SerializerMethodField()
    isUpvoted = serializers.SerializerMethodField()
    isDownvoted = serializers.SerializerMethodField()
    #comments = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ['id', 'posted_by', 'created_at', 'username', 'avatar', 'title', 'description', 'expiry_date', 'isLiked', 'isFollowed', 'isDeletable', 'isUpvoted', 'isDownvoted', 'tags', 'upvotes', 'downvotes', 'price', 'latitude', 'longitude', 'link', 'photos']

    def get_upvotes(self, obj):
        return obj.upvotes.count()

    def get_downvotes(self, obj):
        return obj.downvotes.count()

    def get_photos(self, obj):
        photos = DealPhotos.objects.filter(deal=obj)
        return [photo.photo.url for photo in photos]
    
    def get_username(self, obj):
        user = User.objects.get(pk=obj.posted_by.id)
        return user.username
    
    def get_avatar(self, obj):
        avatar_url = obj.posted_by.avatar.url if obj.posted_by.avatar else None
        return avatar_url
    
    def get_isFollowed(self, obj):
        user = self.context.get('user')
        if user:
            is_followed = user.following.filter(id=obj.posted_by.id).exists()
            return is_followed
        return False


    def get_isLiked(self, obj):
        # Check if the user who liked the deal is provided in the context
        user = self.context.get('user')
        if user:
            return obj.likes.filter(id=user.id).exists()
        return False
    
    def get_isUpvoted(self, obj):
        # Check if the user who liked the deal is provided in the context
        user = self.context.get('user')
        if user:
            return obj.upvotes.filter(id=user.id).exists()
        return False
    
    def get_isDownvoted(self, obj):
        # Check if the user who liked the deal is provided in the context
        user = self.context.get('user')
        if user:
            return obj.downvotes.filter(id=user.id).exists()
        return False
    
    def get_isDeletable(self, obj):
        # Check if the user who liked the deal is provided in the context
        user = self.context.get('user')
        if user == obj.posted_by:
            return True
        if user.role == User.MD:
            return True
        return False
    
    
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
    deals = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['fullname', 'username', 'role', 'followers', 'followings', 'avatar', 'comments', 'deals', 'likes']

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
    
    def get_deals(self, obj):
        deals = Deal.objects.filter(posted_by=obj)
        deal_serializer = DealSerializer(deals, many=True, context={'user': obj})
        return {'deals': deal_serializer.data}
    
    def get_likes(self, obj):
        likes = Deal.objects.filter(likes=obj)
        like_serializer = DealSerializer(likes, many=True, context={'user': obj})
        return {'likes': like_serializer.data}