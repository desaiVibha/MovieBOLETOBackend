from rest_framework import serializers
from django.contrib.auth import authenticate
from movie_app.models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    mobileNumber=serializers.IntegerField()
    class Meta:
        model=User
        fields=('username','password','name','email','mobileNumber')
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            email=validated_data['email'],
            mobileNumber=validated_data['mobileNumber'])
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect username or password")
    
class MovieSerializer(serializers.Serializer):
    class Meta:
        model=Movie
        fields='__all__'

class MovieDetailSerializer(serializers.Serializer):
    class Meta:
        model=MovieDetail
        fields='__all__'

class TheatreSerializer(serializers.Serializer):
    class Meta:
        model=Theatre
        fields='__all__'

class MovieTimingSerializer(serializers.Serializer):
    class Meta:
        model=MovieTiming
        fields='__all__'