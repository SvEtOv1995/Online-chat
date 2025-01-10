from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    room_name = models.CharField(max_length=255)  # Название комнаты
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, отправивший сообщение
    content = models.TextField()  # Текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки сообщения

    def __str__(self):
        return f'{self.user.username} ({self.timestamp}): {self.content}'
