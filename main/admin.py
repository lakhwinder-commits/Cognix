from django.contrib import admin


from .models import Conversation, Message

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'conversation', 'role', 'content', 'timestamp')
    
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)