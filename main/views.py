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