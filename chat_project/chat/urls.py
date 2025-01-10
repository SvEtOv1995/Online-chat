from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_chat_view, name='client_chat'),  # Клиентская страница
    path('send/', views.send_message, name='send_message'),  # Отправка клиентом
    path('admin/chats/', views.admin_chats_view, name='admin_chats'),  # Список чатов для админов
    path('admin/chats/<int:chat_id>/', views.admin_chat_view, name='admin_chat'),  # Конкретный чат для админа
    path('admin/chats/<int:chat_id>/send/', views.admin_send_message, name='admin_send_message'),  # Отправка админом
]
