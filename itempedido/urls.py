from django.urls import path
from . import views

urlpatterns = [
    path('', views.itempedido_list, name='itempedido_list'),
    path('novo/', views.itempedido_create, name='itempedido_create'),
    path('adicionar/<int:item_pk>/', views.adicionar_item, name='adicionar_item'),
    path('<int:pk>/', views.itempedido_detail, name='itempedido_detail'),
<<<<<<< HEAD
    path('<int:pk>/editar/', views.itempedido_update, name='itempedido_update'),
    path('<int:pk>/excluir/', views.itempedido_delete, name='itempedido_delete'),
=======
>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
]
