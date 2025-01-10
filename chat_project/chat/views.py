from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Message

@method_decorator(csrf_exempt, name='dispatch')  # Для обработки POST-запросов # Требуется авторизация
@csrf_exempt
def send_message(request, room_name):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if not message_content:
            return JsonResponse({'error': 'Message content is required'}, status=400)

        message = Message.objects.create(
            user=request.user,
            room_name=room_name,
            content=message_content
        )
        return JsonResponse({
            'user': message.user.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def room(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')  # Загружаем сообщения
    return render(request, 'chat_room.html', {
        'room_name': room_name,
        'messages': messages
    })
