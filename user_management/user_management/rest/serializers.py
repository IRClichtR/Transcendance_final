from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class AppUserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'profile_picture', 'profile_picture_url']
        extra_kwargs = {
            'profile_picture': {'write_only': True}
        }

    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        print("request: ", request)
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None

    def update(self, instance, validated_data):
        print("validated_data: ", validated_data)
        instance.username = validated_data.get('username', instance.username)
        print("instance.username: ", instance.username)
        instance.first_name = validated_data.get('first_Name', instance.first_name)
        print("instance.first_name: ", instance.first_name)
        instance.last_name = validated_data.get('last_Name', instance.last_name)
        print("instance.last_name: ", instance.last_name)
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']
        instance.save()
        return instance
