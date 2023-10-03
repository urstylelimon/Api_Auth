from rest_framework import serializers
from account.models import User

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
        passwword2 = attrs.get('password2')
        if passwword != passwword2:
            raise serializers.ValidationError('Password and Confirm password does not match')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerilazer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']