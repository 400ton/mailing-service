from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'data_created', 'views_count')
    list_filter = ('title',)
    search_fields = ('title', 'views_count')
