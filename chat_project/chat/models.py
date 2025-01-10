from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.user.username if self.user else self.session_id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)  # Привязка к чату
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Кто отправил сообщение (если есть)
    content = models.TextField()  # Содержание сообщения
    is_admin = models.BooleanField(default=False)  # Сообщение от администратора или нет
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки

    def __str__(self):
        return f"{'Admin' if self.is_admin else 'User'}: {self.content[:50]}"
