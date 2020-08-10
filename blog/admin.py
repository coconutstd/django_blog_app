from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'count_text']
    list_display_links = ['title']

    def count_text(self, obj):
        return f'{len(obj.text)}글자'
    count_text.short_description = 'text 글자수'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)