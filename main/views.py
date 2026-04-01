from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request,"index.html")
def about(request):
    return render(request, 'about.html')
def chat(request):
    return render(request, 'chat.html')
def gamezone(request):
    return render(request, 'gamezone.html')

def tools(request):
    return render(request, 'tools.html')

def login(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def save_google_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        picture = response.get('picture')

        if picture:
            from .models import Profile

            
            profile, created = Profile.objects.get_or_create(user=user)

            profile.avatar = picture
            profile.save()


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import Conversation, Message


@login_required
def get_conversations(request):
    convs = Conversation.objects.filter(user=request.user).order_by('-created_at')

    data = []
    for c in convs:
        data.append({
            "id": c.id,
            "title": c.title
        })

    return JsonResponse(data, safe=False)


@login_required
def get_messages(request, conv_id):
    conv = Conversation.objects.get(id=conv_id, user=request.user)

    messages = conv.messages.all().order_by('timestamp')
    data = [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp.timestamp() * 1000
        }
        for m in messages
    ]

    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def create_conversation(request):
    conv = Conversation.objects.create(user=request.user)
    return JsonResponse({"id": conv.id})


@csrf_exempt
@login_required
def save_message(request):
    data = json.loads(request.body)

    conv = Conversation.objects.get(id=data["conversation_id"], user=request.user)

    msg = Message.objects.create(
        conversation=conv,
        user=request.user,
        role=data["role"],
        content=data["content"]
    )

    # update title if first message
    if conv.title == "New Chat" and data["role"] == "user":
        conv.title = data["content"][:30]
        conv.save()

    return JsonResponse({"status": "ok"})