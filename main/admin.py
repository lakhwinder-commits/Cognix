from django.contrib import admin
from .models import Conversation, Message


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'conversation', 'role', 'content', 'timestamp')

    def get_user(self, obj):
        return obj.conversation.user

    get_user.short_description = 'User'


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)