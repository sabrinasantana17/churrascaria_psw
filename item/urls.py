from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('novo/', views.item_create, name='item_create'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('<int:pk>/editar/', views.item_update, name='item_update'),
    path('<int:pk>/excluir/', views.item_delete, name='item_delete'),
]
