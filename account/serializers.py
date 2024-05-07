# from .models import User
# from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken
#
#
# class RegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'username', 'password', 'password2', 'birth', 'sex', 'school']
#
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             username=validated_data['username'],
#             password=validated_data['password']
#         )
#         return user
#
#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#
#         if email and password:
#             user = User.objects.filter(email=email).first()
#             if user and user.check_password(password):
#                 refresh = RefreshToken.for_user(user)
#                 data['refresh'] = str(refresh)
#                 data['access'] = str(refresh.access_token)
#             else:
#                 raise serializers.ValidationError("Invalid email or password.")
#         else:
#             raise serializers.ValidationError("Must include 'email' and 'password'.")
#         return data
