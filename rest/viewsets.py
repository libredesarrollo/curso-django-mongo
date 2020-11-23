from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bson.objectid import ObjectId

from .serializers import BookSerializer, TagSerializer, CategorySerializer
from book.models import Book, Category, Tag, Address

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def set_category(self, request, pk=None):
        
        try:
            book = Book.objects.get(pk=ObjectId(pk))
        except Book.DoesNotExist:
            return Response({'error':'Libro no existe'})

        try:
            category = Category.objects.get(pk=ObjectId(request.data['category_id']))
        except Category.DoesNotExist:
            return Response({'error':'Categoría no existe'})

        book.category = category
        book.save()

        s = BookSerializer(book)
        
        return Response(s.data)

    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk=None):
        
        try:
            book = Book.objects.get(pk=ObjectId(pk))
        except Book.DoesNotExist:
            return Response({'error':'Libro no existe'})

        try:
            tag = Tag.objects.get(pk=ObjectId(request.data['tag_id']))
        except Tag.DoesNotExist:
            return Response({'error':'Tag no existe'})

        book.tags.add(tag)
        book.save()

        s = BookSerializer(book)
        
        return Response(s.data)

    @action(detail=True, methods=['post'])
    def remove_tag(self, request, pk=None):
        
        try:
            book = Book.objects.get(pk=ObjectId(pk))
        except Book.DoesNotExist:
            return Response({'error':'Libro no existe'})

        try:
            tag = Tag.objects.get(pk=ObjectId(request.data['tag_id']))
        except Tag.DoesNotExist:
            return Response({'error':'Tag no existe'})

        book.tags.remove(tag)
        book.save()

        s = BookSerializer(book)
        
        return Response(s.data)

    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        
        try:
            book = Book.objects.get(pk=ObjectId(pk))
        except Book.DoesNotExist:
            return Response({'error':'Libro no existe'})

        if book.addresses is None:
            book.addresses = []

        book.addresses.append(Address(**{ 
            'direction' : request.data['direction'], 
            'country' : request.data['country'] }))

        book.save()

        s = BookSerializer(book)
        
        return Response(s.data)

    @action(detail=True, methods=['post'])
    def remove_address(self, request, pk=None):
        
        try:
            book = Book.objects.get(pk=ObjectId(pk))
        except Book.DoesNotExist:
            return Response({'error':'Libro no existe'})

        if book.addresses is None:
            book.addresses = []

        try:
            index = int(request.data['index'])
        except ValueError:
            return Response({'error':'Indice tiene que ser entero positivo'})

        try:
            book.addresses.pop(index)
        except IndexError:
            return Response({'error':'No puede superar el tamaño máximo de las direcciones'})        

        book.save()

        s = BookSerializer(book)
        
        return Response(s.data)
    
    @action(detail=True, methods=['post'])
    def change_address(self, request, pk=None):
    
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Libro no existe'})

        try:
            index = int(request.data['index'])
        except ValueError:
            return Response({'error': 'Pos debe ser un entero'})

        try:
            book.addresses[index] = Address(**{
                'country' : request.data['country'],
                'direction' : request.data['direction'],
            })
        except IndexError:
            return Response({'error': 'La posición no puede superar el tamaño del array'})
        
        book.save()
        serializer = BookSerializer(book)
        return Response(serializer.data)



