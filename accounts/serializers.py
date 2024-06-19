from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    '''
    Performs :
    - validates if the email is unique in the database.
    - validates if the password and confirm_password fields match.
    - creates a new user instance with validated data and hashed password.
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8,max_length=16, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists. Proceed to login!")
        return value

    def validate(self, attrs):
        print(attrs.get('passsword'))
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'password': 'Password and Confirm Password do not match.'
            })
       
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    '''
    validates if the provided email exists in the database and 
    if the password matches the user's password.
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError({"error":"Incorrect password."})
            else:
                raise serializers.ValidationError({"error":"user does not exist."})

        attrs['user'] = user
        return attrs