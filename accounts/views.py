from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, serializers, status, views, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login
import jwt

from user_profile.serializers import ProfileSerializer
from .serializers import *
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import User

class RegisterView(generics.GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        user1 = request.data
        serializer = self.serializer_class(data=user1)
        serializer.is_valid(raise_exception=True) # Call validate method in serializer
        serializer.save()
        user_data = serializer.data
        profile = UserProfile.objects.get(user=request.user)
        serializer_profile = ProfileSerializer(profile)
        print(serializer_profile.data)


        user = User.objects.get(email=user_data['email'])


        # Make an access token for user
        token = RefreshToken.for_user(user).access_token

        # current_site = get_current_site(request).domain
        # relativeLink = reverse('accounts:email-verify')
        # absurl = 'http://' +  current_site + relativeLink + "?token=" + str(token)
        # email_body = 'Hi ' + user.first_name + ' Use linke below to veriy your email \n' + absurl
        # data = {'email_body': email_body, 'email_subject': 'Verify your email', 'to_email': user.email}
        # Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)



class VerifyEmail(views.APIView):
    """
    After Registration view, if user verified his/her account
    with the email we sent, then user's account is activate and verified.
    """
    serializer_class = PhoneVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                           description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            # decode the token to get the user by id
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """Login View"""
    serializer_class = LoginSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)


        return Response(serializers.data, status=status.HTTP_200_OK)


class RequestPasswordResetPhone(generics.GenericAPIView):
    """Resquest Passwrod Reset Email View"""
    serializer_class = ResetPasswordPhoneRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Because we need to make a reset password link and we don't want to
            # others can see the id because of security issues
            # So we encode it with base64
            # uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            # token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request).domain
            # relativeLink = reverse('accounts:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            #
            # redirect_url = request.data.get('redirect_url', '')  # Added recently
            #
            # # Send reset password link to user
            # absurl = 'http://' + current_site + relativeLink
            # email_body = 'Hello\n Use link below to reset your password\n' + absurl + '?redirect_url=' + redirect_url
            # data = {'email_body': email_body, 'email_subject': 'Reset your password', 'to_email': user.email}
            # Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No Such User with this email, Please register first'},
                            status=status.HTTP_404_NOT_FOUND)


# class PasswordTokenCheckAPIView(generics.GenericAPIView):
#     """Check validation of token view"""
#     serializer_class = SetNewPasswordSerializer

#     def get(self, request, uidb64, token):

#         redirect_url = request.GET.get('redirect_url')
#         # redirect_url = '/accounts/password-reset-complete'

#         try:
#             # decode user id and get user
#             user_id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=user_id)

#             # check wether the token is associated with user or not
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 if len(redirect_url) > 3:
#                     return CustomeRedirect(redirect_url + '?token_valid=False')
#                 else:
#                     return CustomeRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

#             if redirect_url and len(redirect_url) > 3:
#                 return CustomeRedirect(
#                     redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
#             else:
#                 return CustomeRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

#         except DjangoUnicodeDecodeError:
#             try:
#                 if not PasswordResetTokenGenerator().check_token(user):
#                     return Response(redirect_url + '?token_valid=False')
#             except UnboundLocalError as e:
#                 return Response({'error': 'Token is not valid, please request a new one'},
#                                 status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """Set new password view"""

    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    """Log out user with refresh token"""

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'Successfully loged out'}, status=status.HTTP_204_NO_CONTENT)