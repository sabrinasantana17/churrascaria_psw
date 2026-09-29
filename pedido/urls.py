from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('novo/', views.pedido_create, name='pedido_create'),
    path('<int:pk>/', views.pedido_detail, name='pedido_detail'),
    path('<int:pk>/concluir/', views.concluir_pedido, name='concluir_pedido'),
]
