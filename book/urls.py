from django.urls import path

from . import views

app_name='book'
urlpatterns = [
    path('', views.index, name='index' ),
    path('book/add', views.add, name='add' ),
    path('book/update/<str:pk>', views.update, name='update' ),
    path('book/delete/<str:pk>', views.delete, name='delete' ),
    path('book/j-get-book-by-id/<str:pk>', views.jgetBookById)
]