from django.contrib import admin
from .models import EmailLog

# Register your models here.
@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'sent_at', 'success')
    search_fields = ('user__email', 'subject')
    list_filter = ('success', 'sent_at')