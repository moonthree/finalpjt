from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    ),

    token = serializers.CharField(max_length=255, read_only=True),

    def create(self, validated_data):
        print(validated_data)
        # user = User.objects.create_user(
        #     username=validated_data['username'],
        #     nickname=validated_data['nickname'],
        #     password=validated_data['password']
        # )
        # return user
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            'username',
            'nickname',
            'password',
            'token'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class LoginSerializer(serializers.Serializer):
#     # 1.
#     username = serializers.CharField(max_length=255, write_only=True)
#     password = serializers.CharField(max_length=128, write_only=True)

#     # 2.
#     def validate(self, data):
#         username = data.get('username', None)
#         password = data.get('password', None)

#         # 3.
#         if username is None:
#             raise serializers.ValidationError(
#                 'An username is required to log in.'
#             )

#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )

#         # 4.
#         user = User(username=username, password=password)

#         # 5.
#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this username and password was not found'
#             )

#         if not user.is_active:
#             raise serializers.ValidationError(
#                 'This user has been deactivated.'
#             )

#         # 6.

#         # 7.
#         return {
#             'username': user.username,
#             'last_login': user.last_login
#         }
