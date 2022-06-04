from rest_framework import serializers

from .models import Product, LikeProduct, Review


class ProductSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.title
        representation['owner'] = instance.owner.email
        representation['likes'] = instance.likes.all().count()
        representation['reviews'] = instance.reviews.all().count()
        return representation


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = ('author', )

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = instance.product.title
        representation['author'] = instance.author.email
        return representation


class LikeProductSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeProduct
        fields = '__all__'
