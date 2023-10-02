from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from account.serializers import UserRegistrationSerializer




@api_view(['GET'])
def user_registration(request, format=None):
    if request.method == 'GET':
        serializer = UserRegistrationSerializer(data = requst.data)

        return Response({'msg': 'Registration Successfully'})
