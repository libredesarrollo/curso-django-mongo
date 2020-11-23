from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from django.urls import path

from .viewsets import BookViewset, CategoryViewset, TagViewset
from . import views

urlpatterns = [
    path('login', views.login),
    path('obtain-jwt-token', obtain_jwt_token),
    path('verify-jwt-token', verify_jwt_token),
    path('refresh-jwt-token', refresh_jwt_token)
]

route = routers.SimpleRouter()

route.register('book',BookViewset)
route.register('category',CategoryViewset)
route.register('tag',TagViewset)

urlpatterns += route.urls