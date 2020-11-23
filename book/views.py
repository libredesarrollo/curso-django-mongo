from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse

from bson.objectid import ObjectId

from .models import Book, Category, Tag
from .forms import BookForm

#-------- CRUD

def index(request):
    return _listBook(request, BookForm())

def add(request):

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return _listBook(request, form)

    return redirect('book:index')

def update(request, pk):

    book = Book.objects.get(pk=ObjectId(pk))

    if request.method == 'POST':

        # ----- prueba editar POST
        #request.POST._mutable = True
        #request.POST['category'] = ObjectId(request.POST['category'])
        #print(request.POST['category'])
        
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        else:
            return _listBook(request, form)

    return redirect('book:index')

def delete(request,pk):

    try:
        book = Book.objects.get(pk=ObjectId(pk))
        book.delete()
    except Book.DoesNotExist:
        pass

    return redirect('book:index')

#-------- pruebas

def uno_a_muchos(pk):
    book = Book.objects.get(pk=ObjectId(pk))
    category = Category.objects.get(pk=ObjectId("5f621f0d2c20271a2f84f3c9"))

    book.category = category
    print(book.category)
    book.save()

def unos_a_muchos_documentos_embebidos(pk):
    book = Book.objects.get(pk=ObjectId(pk))

    book.addresses = [
        {
            '_id' : ObjectId(),
            'direction' : 'Dirección del libro',
            'country' : 'España'
        },
        {
            '_id' : ObjectId(),
            'direction' : 'Dirección del libro 2',
            'country' : 'Venezuela'
        }
    ]

    book.save()

    print(book.addresses[0]['direction'])

def muchos_a_muchos(pk):
    book = Book.objects.get(pk=ObjectId(pk))
    book.tags.add(Tag.objects.all()[0])
    book.save()
    
def uno_a_uno_documentos_embebidos(pk):

    print(book.dimention)

    book.dimention = {
        '_id': ObjectId(),
        'x' : 10,
        'z' : 5,
        'y' :20
    }

    print(book.dimention['x'])
    book.dimention['x'] = 11
    print(book.dimention['x'])
    book.save()

#-------- privados

def _listBook(request, form):
    books = Book.objects.all()
    paginator = Paginator(books,2)

    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    
    return render(request, 'book/index.html',{'books':books_page, 'form': form})


#-------- json
def jgetBookById(request,pk):

    try:
        book = Book.objects.get(pk=ObjectId(pk))
    except Book.DoesNotExist:
        return JsonResponse("")

    return JsonResponse({
        'name': book.name,
        'content': book.content,
        'category_id': str(book.category._id),
        'dimention': {
            'x':book.dimention.x,
            'z':book.dimention.y,
            'y':book.dimention.y,
        }
    })