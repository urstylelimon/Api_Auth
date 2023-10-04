from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from account.serializers import UserRegistrationSerializer,UserLoginSerilazer,UserProfileSerializer,ChangePasswordSerializer,PasswordResetSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#Genarate Token Menually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
 # Specify the custom renderer here
@renderer_classes([UserRenderer])

def user_registration(request, format=None):
     

    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg': 'Registration Successfully'},
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
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg': 'LogIn Successfully'},
                                    status= status.HTTP_200_OK)
            else:

                # Create a custom error response with 'ErrorDetail' key
                error_response = {'Error': "Enter Correct email and Password"}
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])

def UserView(request,format = None):
    serializer = UserProfileSerializer(request.user)
    # if serializer.is_valid():
    return Response(serializer.data,status=status.HTTP_200_OK)

#Password Reset

@api_view(["POST"])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])

def ChangePassword(request,format = None):
        
        serializer = ChangePasswordSerializer(data = request.data,context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'passsword Change Successfullly'  })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])

def PasswordReset(request,format = None):
    serializer = PasswordResetSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        return Response({
            'msg':'Password Reset link send.Please check your mail.'
        },status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])
def UserPasswordResetView(request, uid, token, format = None):
    serilazir = UserPasswordResetSerializer(data=request.data,
                                            context = {'uid':uid,'token':token})
    if serilazir.is_valid(raise_exception=True):
        return Response({'msg':'Password Reset Successfully'},
                        status=status.HTTP_200_OK)
    return Response(serilazir.errors,status=status.HTTP_400_BAD_REQUEST)
    




    
