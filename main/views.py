from django.shortcuts import render
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .models import Conversation, Message


# ---------- PAGE VIEWS ----------
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, 'about.html')


@login_required
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


# ---------- GOOGLE AVATAR ----------
def save_google_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        picture = response.get('picture')
        if picture:
            from .models import Profile
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.avatar = picture
            profile.save()


# ---------- API VIEWS ----------

@login_required
def get_conversations(request):
    convs = Conversation.objects.filter(user=request.user).order_by('-created_at')
    data = [{"id": c.id, "title": c.title} for c in convs]
    return JsonResponse(data, safe=False)


@login_required
def get_messages(request, conv_id):
    try:
        conv = Conversation.objects.get(id=conv_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    messages = conv.messages.all().order_by('timestamp')

    data = [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": int(m.timestamp.timestamp() * 1000)
        }
        for m in messages
    ]

    return JsonResponse(data, safe=False)


@login_required
def create_conversation(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    conv = Conversation.objects.create(user=request.user)
    return JsonResponse({"id": conv.id})


@login_required
def save_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Prevent empty messages
    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Empty message"}, status=400)

    try:
        conv = Conversation.objects.get(id=data["conversation_id"], user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({"error": "Invalid conversation"}, status=404)

    Message.objects.create(
        conversation=conv,
        role=data["role"],
        content=content
    )

    # Auto update title
    if conv.title == "New Chat" and data["role"] == "user":
        conv.title = content[:30]
        conv.save()

    return JsonResponse({"status": "ok"})


@login_required
def delete_conversation(request, conv_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        conv = Conversation.objects.get(id=conv_id, user=request.user)
        conv.delete()
        return JsonResponse({"status": "success"})
    except Conversation.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)


@login_required
def update_conversation_title(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        conv = Conversation.objects.get(id=data["conversation_id"], user=request.user)
        conv.title = data["title"].strip()
        conv.save()
        return JsonResponse({"status": "updated"})
    except Conversation.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)