from rest_framework import serializers
from account.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class  UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'},
                                      write_only = True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }

#validiting Password
    def validate(self,attrs):
        passwword = attrs.get('password')
        password2 = attrs.get('password2')
        if passwword != password2:
            raise serializers.ValidationError('Password and Confirm password does not match')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

#LogIn
class UserLoginSerilazer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

#Password Change
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and Confirm password do not match')

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance
    

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('passwor reset link',link)

            #send email
            body = 'Click following Link to Reset Your Password'+ link
            data = {
                'subject':'Reset Your password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs

        else:
            raise ValidationErr('You are not a register user.')

class UserPasswordResetSerializer(serializers.ModelSerializer):
    try:


        password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
        password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

        class Meta:
            model = User
            fields = ['password', 'password2']

        def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')


            if password != password2:
                raise serializers.ValidationError('Password and Confirm password do not match')
            id  = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('Token is not valid or Expired')
            user.set_password(password)
            user.save()

            return attrs
    except DjangoUnicodeDecodeError as identifier:
        PasswordResetTokenGenerator().check_token(user,token)
        raise ValidationErr('Token is not valid or Expired')
