from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('novo/', views.pedido_create, name='pedido_create'),
]