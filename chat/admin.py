from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'timestamp', 'avatar_color')
    ordering = ('-timestamp',)
