from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from .models import Message

def index(request):
    """
    Render the main chat page.
    Passes existing messages to the template for initial load.
    """
    # Get last 7 messages, but we need them in chronological order for display
    # So we get last 7 (ordered by -timestamp) and then reverse them
    messages = Message.objects.order_by('-timestamp')[:7]
    messages = reversed(messages)
    
    # Format for template
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            'text': msg.text,
            'timestamp': msg.timestamp.strftime("%H:%M"),
            'avatar_color': msg.avatar_color
        })
        
    return render(request, 'chat/index.html', {'messages': formatted_messages})

@csrf_exempt
def send_message(request):
    """
    API endpoint to add a message to the database.
    Enforces Circular Queue logic (Max 7).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('message')
            if text:
                # 1. Check limit and delete oldest if needed
                # We want max 7, so if we have 7 or more, delete the oldest
                # Note: This is a simple check. In high concurrency, might need locking, 
                # but for this app it's fine.
                current_count = Message.objects.count()
                if current_count >= 7:
                    # Delete oldest
                    oldest = Message.objects.order_by('timestamp').first()
                    if oldest:
                        oldest.delete()

                # 2. Create new message
                colors = ['#6366f1', '#ef4444', '#10b981', '#f59e0b', '#3b82f6', '#ec4899']
                avatar_color = random.choice(colors)
                
                Message.objects.create(
                    text=text,
                    avatar_color=avatar_color
                )
                
                return JsonResponse({'status': 'success', 'message': 'Message sent'})
            return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def get_messages(request):
    """
    API endpoint to retrieve all messages.
    """
    # Get last 7, reversed to be chronological
    messages = Message.objects.order_by('-timestamp')[:7]
    messages = reversed(messages)
    
    data = []
    for msg in messages:
        data.append({
            'text': msg.text,
            'timestamp': msg.timestamp.strftime("%H:%M"),
            'avatar_color': msg.avatar_color
        })
        
    return JsonResponse({'messages': list(data)})

@csrf_exempt
def delete_message(request):
    """
    API endpoint to delete the oldest message.
    """
    if request.method == 'POST':
        oldest = Message.objects.order_by('timestamp').first()
        if oldest:
            text = oldest.text
            oldest.delete()
            return JsonResponse({'status': 'success', 'removed': text})
        return JsonResponse({'status': 'error', 'message': 'Queue is empty'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
