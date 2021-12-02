from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from user_profile.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'password')
        extra_kwargs = {'name': {'required': True}}

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        name = attrs.get('name', '')
        # last_name = attrs.get('last_name', '')

        # Validation of data which user add
        if not email:
            raise serializers.ValidationError('You should add an email')
        if not name:
            raise serializers.ValidationError('You should add your name')
        # if not last_name:
        #     raise serializers.ValidationError('You should add your last name')
        if not username:
            raise serializers.ValidationError('You should add your username')
        return attrs

    # After validation we create a new user with his/her profile
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class PhoneVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)


    class Meta:
        model = User
        fields = ('token',)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'tokens')

    def get_tokens(self, obj):
        """A method for returning the tokens"""

        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # Add recently
        filtered_user_by_email = User.objects.filter(email=email)

        user = auth.authenticate(email=email, password=password)

        # Here we want to be sure that login process is with email not google account or other login ways
        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
        detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider
        )

        if not user:
            raise AuthenticationFailed('Invalid Credentials, try agian!')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('email is not verified')
        return {
            'email': user.email,
            'tokens': user.tokens()
        }


class ResetPasswordPhoneRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ('email',)


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ('password', 'token', 'uidb64')

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            token = attrs.get('token', '')
            uidb64 = attrs.get('uidb64', '')
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The raset link is invalid', 401)

            # Save password as hash
            user.set_password(password)
            user.save()
            return user

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # Because access token expire very soon
            # so we set user's refresh token in black list
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class AdminLoginSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        fields = ('email', 'password')