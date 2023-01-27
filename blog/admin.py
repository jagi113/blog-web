from django.contrib import admin
from .models import Post, Tag, Author, Comment



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",) }
    list_filter = ("author", "tags")
    list_display = ("title", "author")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "commented_post", "user_name", "created_on")
    
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)