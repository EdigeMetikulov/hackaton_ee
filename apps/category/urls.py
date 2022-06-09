from django.urls import path

from .views import ListCreateCategoryView

urlpatterns = [
    path('list/', ListCreateCategoryView.as_view()),
]