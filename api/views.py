from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Article, Category
from .serializers import ArticlesSerializer, CategorySerializer


class ArticleView(APIView):

    def get(self, request):
        orders = Article.objects.all()
        serializer = ArticlesSerializer(orders, many=True)
        return Response({"Articles": serializer.data})


class CategoryView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"Categories": serializer.data})