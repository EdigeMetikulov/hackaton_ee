from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (ListCreateProductView, GetProductView,
                    UpdateProductView, DestroyProductView,
                    LikeProductView, ReviewViewSet)

router = SimpleRouter()
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('list_or_create/', ListCreateProductView.as_view()),
    path('<int:pk>/', GetProductView.as_view()),
    path('delete/<int:pk>/', DestroyProductView.as_view()),
    path('update/<int:pk>/', UpdateProductView.as_view()),
    path('<int:pk>/like/', LikeProductView.as_view()),
    path('', include(router.urls)),
]
