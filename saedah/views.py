from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Comments, DealPhotos, User, Deal
from django.contrib.auth import authenticate
from .serializers import CommentSerializer, UserCustomSerializer, UserSerializer, DealSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','POST'])
def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse({'users':serializer.data})
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def deals_list(request):
    if request.method == 'GET':
        deal = Deal.objects.all()
        serializer = DealSerializer(deal, many=True)
        return JsonResponse({'deals':serializer.data})
    if request.method == 'POST':
        user = request.user
        data = request.data.copy()
        data['posted_by'] = user.id

        # Get the list of uploaded images from the request
        photos = request.FILES.getlist('photos')

        # Create a new deal instance
        serializer = DealSerializer(data=data)

        if serializer.is_valid():
            # Save the deal object with the user as the creator
            deal = serializer.save()

            # Loop through the list of images and create DealPhotos objects
            for photo in photos:
                deal_photo = DealPhotos(deal=deal, photo=photo)
                deal_photo.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])  # Added PUT and DELETE methods
@permission_classes([IsAuthenticated])
def deal_detail(request, id):
    user = request.user
    try:
        deal = Deal.objects.get(pk=id)
    except Deal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to modify the deal (PUT/DELETE)
    if request.method in ['PUT', 'DELETE']:
        if user != deal.posted_by and user.role != User.MD:
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = DealSerializer(deal)
        if user in deal.likes.all():
            deal.isLiked = True
        return Response({'deal': serializer.data})

    if request.method == 'PUT':
        # Assuming you have a DealSerializer for updating the deal details
        serializer = DealSerializer(deal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Deal details updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        deal.delete()
        return Response({'message': 'Deal deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#PROFILE INFO  
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserCustomSerializer(user)
        return JsonResponse({'user':serializer.data})
        
#EDITING PROFILE INFO
    elif request.method == 'PUT':
        fullname = request.data.get('fullname')
        username = request.data.get('username')
        serializer = UserCustomSerializer(user, data={"fullname": fullname, "username": username}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Profile Details for a specified user
@api_view(['GET'])
def profile_detail(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserCustomSerializer(user)
        return JsonResponse({'user':serializer.data})
    

#A user profile deals for a specified user
@api_view(['GET'])
def profile_deals(request, id):

    user = get_object_or_404(User, id=id)
    
    if request.method == 'GET':
        deals = Deal.objects.filter(posted_by=user)
        serializer = DealSerializer(deals, many=True)
        return JsonResponse({'user':serializer.data})
    
#Follow
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_or_unfollow_profile(request, id):
    target_user = get_object_or_404(User, id=id)
    current_user = request.user

    if target_user == current_user:
        return Response({'detail': 'You cannot follow or unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    if current_user in target_user.followers.all():
        target_user.followers.remove(current_user)
        action = 'unfollowed'
    else:
        target_user.followers.add(current_user)
        action = 'followed'

    return Response({'detail': f'You have {action} {target_user.fullname}'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_followings(request, id):
    target_user = get_object_or_404(User, id=id)
    follower_users = target_user.following.all()
    serializer = UserCustomSerializer(follower_users, many=True)
    return Response({'followings': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_followers(request, id):
    target_user = get_object_or_404(User, id=id)
    following_users = target_user.followers.all()
    serializer = UserCustomSerializer(following_users, many=True)
    return Response({'followers': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_user_image(request):
    current_user = request.user
    image = request.data.get('image')  # Assuming the image is sent as a file in the request data

    if not image:
        return Response({'error': 'Image file not provided'}, status=400)

    current_user.avatar = image
    current_user.save()

    serializer = UserCustomSerializer(current_user)
    return Response({'user': serializer.data})

#Upvotes and Downvotes
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote_deal(request, id):
    deal = get_object_or_404(Deal, id=id)
    user = request.user

    if user in deal.upvotes.all():
        return Response({'error': 'You have already upvoted this deal.'}, status=400)

    deal.upvotes.add(user)
    deal.save()

    return Response({'message': 'Upvoted successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote_deal(request, id):
    deal = get_object_or_404(Deal, id=id)
    user = request.user

    if user in deal.downvotes.all():
        return Response({'error': 'You have already downvoted this deal.'}, status=400)

    deal.downvotes.add(user)
    deal.save()

    return Response({'message': 'Downvoted successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_deal(request, id):
    deal = get_object_or_404(Deal, id=id)
    user = request.user

    if user in deal.likes.all():
        deal.likes.remove(user)
        return Response({'message': 'Unliked successfully.'})

    deal.likes.add(user)
    deal.save()

    return Response({'message': 'Liked successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_deal(request, id):
    try:
        deal = Deal.objects.get(id=id)
    except Deal.DoesNotExist:
        return Response({'error': 'Deal not found'}, status=404)

    user = request.user
    content = request.data.get('content', None)

    if not content:
        return Response({'error': 'Comment content is required'}, status=400)

    comment_data = {
        'Deal_id': deal.id,
        'posted_by': user.id,
        'content': content,
    }
    serializer = CommentSerializer(data=comment_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET','PUT', 'DELETE'])  # Adding PUT and DELETE methods
@permission_classes([IsAuthenticated])
def comment_removeoredit(request, id):
    user = request.user
    try:
        comment = Comments.objects.get(pk=id)
    except Comments.DoesNotExist:
        return Response({'message': 'This comment does not exist.'},status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to modify the comment (PUT/DELETE)
    if request.method in ['PUT', 'DELETE']:
        if user != comment.posted_by and user.role != User.MD:
            return Response({'message': 'You are not authorized.'},status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        comments = Comments.objects.filter(id=id)
        serializer = CommentSerializer(comments, many=True)
        return Response({'comments': serializer.data})
    
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Comment updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def show_user_comments(request, id):
    comments = Comments.objects.filter(posted_by=id)
    serializer = CommentSerializer(comments, many=True)
    return Response({'comments': serializer.data})