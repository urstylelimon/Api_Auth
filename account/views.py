from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from account.serializers import UserRegistrationSerializer,UserLoginSerilazer
from django.contrib.auth import authenticate


@api_view(['POST'])
def user_registration(request, format=None):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration Successfully'},
                            status= status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def UserLoginView(request,format = None):

    if request.method == 'POST':
        serializer = UserLoginSerilazer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email,password = password)
            if user is not None:
                return Response({'msg': 'LogIn Successfully'},
                                    status= status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_feild_errors':['Email or password is not valid']}},
                                    status= status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
