from django.urls import path
from .views import LoginView, RegisterView, ActivateView, ForgetPasswordView, LogoutAPIView

# http://127.0.0.1:8000/api/v1/account
urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("activate/<str:activate_code>/", ActivateView.as_view()),
    path("forget_password/", ForgetPasswordView.as_view()),
    path("logout/", LogoutAPIView.as_view()),

]
