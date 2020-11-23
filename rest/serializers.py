#from rest_framework import serializers
from rest_meets_djongo import serializers

from book.models import Book, Category, Tag

class CategorySerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Category
        fields = ('_id','name') 

class TagSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Tag
        fields = ('_id','name') 

class BookSerializer(serializers.DjongoModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = ('_id','name','content','dimention','addresses','category','tags') 

