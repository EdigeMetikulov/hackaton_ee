from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import CustomAuthTokenSerializer, RegisterSerializer, ForgetPasswordSerializer
from .services.utils import send_activate_code, send_new_password

User = get_user_model()  # внутри лежит AUTH_USER_MODEL


class LoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class RegisterView(APIView):

    def post(self, request):
        data = request.POST  # (email=adadsd@mail.ru, password =!@#!@$@)
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data #dict <---- is_valid()
        user: CustomUser = serializer.save()
        send_activate_code(user.activate_code, user.email)
        return Response(serializer.data)


class ActivateView(APIView):
    # http://127.0.0.1:8000/api/v1/account/activate/afghaffafsada
    def get(self, request, activate_code):
        user = get_object_or_404(CustomUser, activate_code=activate_code)
        user.is_active = True
        user.save()
        return Response("activated!")


class ForgetPasswordView(APIView):

    def post(self, request):
        data = request.POST
        serializer = ForgetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user: CustomUser = User.objects.get(email=email)
        new_password = user.generate_activation_code(10, 'qwergafsg57')
        user.set_password(new_password)
        user.save()
        send_new_password(email, new_password)
        return Response({'message': 'your new password was send to email'}, status=status.HTTP_200_OK)


# class LogoutAPIView(APIView):
#     def get(self, request, token):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    def get(self, request):
        user = request.user
        print(request.user.is_authenticated)
        token = Token.objects.get(user=user)
        token.delete()
        # return HttpResponseRedirect('product')
        return Response('logout', status=status.HTTP_401_UNAUTHORIZED)
