from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "pk", "creator", "number_from", "number_to", "kind",
        "created_at", "has_blocked", "has_error",
    ]
    list_filter = ["kind", "created_at", "has_blocked", "has_error"]
    search_fields = ["number_from", "number_to", "content"]
