from rest_framework import serializers


class ArticlesSerializer(serializers.Serializer):
    category_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    user_id = serializers.CharField()
    date = serializers.CharField()
    views = serializers.CharField()


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField()
    subcategory = serializers.CharField()