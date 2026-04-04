"""
URL configuration for cognix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from main import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('MasterLogin/', admin.site.urls),
    path('',views.home),
    path('about/', views.about),
    path('chat/', views.chat),
    path('gamezone/', views.gamezone, name='gamezone'),
    path('tools/', views.tools, name='tools'),
    path('login/', views.login, name='login'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', views.logout_view, name='logout'),
    path("api/conversations/", views.get_conversations),
    path("api/messages/<int:conv_id>/", views.get_messages),
    path("api/create-conversation/", views.create_conversation),
    path("api/save-message/", views.save_message),
    path('api/delete-conversation/<int:conv_id>/', views.delete_conversation),
    path("api/update-conversation-title/", views.update_conversation_title),
]
