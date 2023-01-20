from django.contrib import admin
from .models import Post, Tag, Author



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",) }
    list_filter = ("author", )
    list_display = ("title", "author")
    
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Author)