"""
Author: Juan Pablo Rivera Velasco
Version: 1.0
Correo: jpablo.localhost@gmail.com
Se definen los serializadores que permiten interactuar con los modelos, y la representación de los mismos
"""
from rest_framework import serializers
import hashlib
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

from backend.models import Users


from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    activation = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'activation': self.validated_data.get('activation', ''),
        }

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','email','name','activation')
        read_only_fields = ('email',)

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)


    def create(self, validated_data):

        user = UserModel.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.name = self.validated_data.get('name', '')
        seed = "sdxfsedrtxcdftdfgbcdfgd"+user.email
        user.activation = hashlib.md5(seed.encode()).hexdigest()
        user.save()

        subject = 'Gracias por registrarte'
        message = 'A continuacion tu codigo de activascion: ' + user.activation
        email_from = 'no-reply@cappfe.com'
        recipient_list = [user.email,]
        send_mail( subject, message, email_from, recipient_list )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "email", "password", "name" )
