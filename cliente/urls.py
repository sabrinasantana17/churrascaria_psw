from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('novo/', views.cliente_create, name='cliente_create'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('<int:pk>/', views.cliente_detail, name='cliente_detail'),
]