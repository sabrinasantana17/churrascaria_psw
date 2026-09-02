from django.urls import path
from . import views

urlpatterns = [
    path('', views.itempedido_list, name='itempedido_list'),
    path('novo/', views.itempedido_create, name='itempedido_create'),
]