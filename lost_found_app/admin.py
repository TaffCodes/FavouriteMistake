from django.contrib import admin
from .models import EmailLog, ItemMatch, LostItem, FoundItem

# Register your models here.
@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'sent_at', 'success')
    search_fields = ('user__email', 'subject')
    list_filter = ('success', 'sent_at')

@admin.register(ItemMatch)
class ItemMatchAdmin(admin.ModelAdmin):
    list_display = ('lost_item', 'found_item', 'match_score', 'created_at', 'match_level')
    search_fields = ('lost_item__name', 'found_item__name')
    list_filter = ('match_score', 'created_at', 'status')

    def match_level(self, obj):
        if obj.match_score > 0.6:
            return 'High match'
        elif obj.match_score > 0.2:
            return 'Medium match'
        else:
            return 'Low match'
    match_level.short_description = 'Match Level'

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'reported_at', 'is_matched')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)
    


    def is_matched(self, obj):
        return ItemMatch.objects.filter(lost_item=obj).exists()
    is_matched.boolean = True
    is_matched.short_description = 'Matched'

@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'reported_at', 'is_matched')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)
    

    def is_matched(self, obj):
        return ItemMatch.objects.filter(found_item=obj).exists()
    is_matched.boolean = True
    is_matched.short_description = 'Matched'