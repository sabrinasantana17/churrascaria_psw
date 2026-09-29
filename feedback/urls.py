from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('novo/', views.feedback_create, name='feedback_create'),
    path('<int:pk>/', views.feedback_detail, name='feedback_detail'),
    path('<int:pk>/editar/', views.feedback_update, name='feedback_update'),
    path('<int:pk>/excluir/', views.feedback_delete, name='feedback_delete'),
]
