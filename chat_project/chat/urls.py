from django.urls import path
from . import views

urlpatterns = [
   path('<str:room_name>/', views.room, name='room'),
   path('<str:room_name>/send/', views.send_message, name='send_message'),
]

