from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer
from .permission import IsAdminOrAllowAny


class ListCreateCategoryView(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminOrAllowAny, )