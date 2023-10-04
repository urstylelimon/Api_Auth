from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from account.serializers import UserRegistrationSerializer,UserLoginSerilazer
from django.contrib.auth import authenticate
from account.renders import UserRenderer


@api_view(['POST'])
 # Specify the custom renderer here
@renderer_classes([UserRenderer])

def user_registration(request, format=None):
     

    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'msg': 'Registration Successfully'},
                            status= status.HTTP_201_CREATED)
        else:
            # Create a custom error response with 'ErrorDetail' key
            error_response = {'Error': serializer.errors}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["POST"])
@renderer_classes([UserRenderer])

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

                # Create a custom error response with 'ErrorDetail' key
                error_response = {'Error': "Enter Correct email and Password"}
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
