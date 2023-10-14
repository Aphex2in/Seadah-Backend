from django.http import JsonResponse
from .models import User, Deal
from django.contrib.auth import authenticate
from .serializers import UserSerializer, DealSerializer
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
        user_id = request.user.id # Get the user's ID from the request data.
        request.data['posted_by'] = user_id  # Assign the user's ID to the 'posted_by' field.
        serializer = DealSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    user = request.user
    if request.method == 'GET':
        try:
            user_info = {
                'fullname': user.fullname,
                'username': user.username,
                'role': user.role
            }
            return Response(user_info)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#EDITING PROFILE INFO
    elif request.method == 'PUT':
        fullname = request.data.get('fullname')
        username = request.data.get('username')
        serializer = UserSerializer(user, data={"fullname": fullname, "username": username}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)