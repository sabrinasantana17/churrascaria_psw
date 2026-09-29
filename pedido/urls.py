from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('novo/', views.pedido_create, name='pedido_create'),
    path('<int:pk>/', views.pedido_detail, name='pedido_detail'),
<<<<<<< HEAD
    path('<int:pk>/editar/', views.pedido_update, name='pedido_update'),
    path('<int:pk>/excluir/', views.pedido_delete, name='pedido_delete'),
=======
>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
    path('<int:pk>/concluir/', views.concluir_pedido, name='concluir_pedido'),
]
