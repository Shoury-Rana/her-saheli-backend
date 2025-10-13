from django.contrib import admin
from .models import StaticContent

@admin.register(StaticContent)
class StaticContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'relevant_mode', 'content_type', 'week_of_pregnancy')
    list_filter = ('relevant_mode', 'content_type')
    search_fields = ('title', 'body')
    ordering = ('relevant_mode', 'content_type', 'title')
    list_per_page = 25