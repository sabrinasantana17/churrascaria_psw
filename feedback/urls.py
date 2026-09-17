from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('novo/', views.feedback_create, name='feedback_create'),
    path('<int:pk>/', views.feedback_detail, name='feedback_detail'),
]