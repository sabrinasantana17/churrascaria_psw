from django.urls import path
from . import views

urlpatterns = [
    path('', views.funcionario_list, name='funcionario_list'),
    path('novo/', views.funcionario_create, name='funcionario_create'),
]