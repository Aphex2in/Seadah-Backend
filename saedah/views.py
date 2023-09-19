from django.http import JsonResponse
from .models import User
from .serializers import SaedahSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET','POST'])
def saedah_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = SaedahSerializer(user, many=True)
        return JsonResponse({'users':serializer.data})
    
    if request.method == 'POST':
        serializer = SaedahSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)