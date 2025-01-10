import uuid
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Chat, Message

def get_or_create_chat(request):
    """Получить или создать чат для текущего клиента."""
    session_id = request.COOKIES.get('session_id')

    # Если нет session_id в cookies, создаем новый
    if not session_id:
        session_id = str(uuid.uuid4())  # Генерация нового session_id

    # Получаем или создаем чат с этим session_id
    chat, created = Chat.objects.get_or_create(session_id=session_id)
    
    return chat, created, session_id


def client_chat_view(request):
    """Корневая страница клиента для отправки сообщений."""
    chat, created, session_id = get_or_create_chat(request)
    messages = chat.messages.order_by('timestamp')
    response = render(request, 'chat/client_chat.html', {'messages': messages})
    if created:
        response.set_cookie('session_id', session_id)  # Установить куку с session_id
    return response


@csrf_exempt
def send_message(request):
    """Обработка отправки сообщений клиентом."""
    if request.method == 'POST':
        chat, _, _ = get_or_create_chat(request)
        message_content = request.POST.get('message')
        if not message_content:
            return JsonResponse({'error': 'Message content is required'}, status=400)

        message = Message.objects.create(
            chat=chat,
            user=None,  # Сообщение от анонимного клиента
            content=message_content,
            is_admin=False
        )
        return JsonResponse({
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def admin_chats_view(request):
    """Страница для администраторов со списком всех чатов."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    chats = Chat.objects.all().order_by('-created_at')
    return render(request, 'chat/admin_chats.html', {'chats': chats})


@login_required
def admin_chat_view(request, chat_id):
    """Страница администратора для конкретного чата."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.order_by('timestamp')
    return render(request, 'chat/admin_chat.html', {'chat': chat, 'messages': messages})


@csrf_exempt
@login_required
def admin_send_message(request, chat_id):
    """Администратор отправляет сообщение в чат."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        message_content = request.POST.get('message')
        if not message_content:
            return JsonResponse({'error': 'Message content is required'}, status=400)

        message = Message.objects.create(
            chat=chat,
            user=request.user,
            content=message_content,
            is_admin=True
        )
        return JsonResponse({
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)
