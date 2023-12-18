from django.contrib import admin
from .models import Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "pub_date", "author")
    list_filter = ("pub_date",)
    search_fields = ("title",)
    empty_value_display = "-empty-"


class LikeAdmin(admin.ModelAdmin):
    list_display = ("pk", "post", "user", "value", "date")
    list_filter = ("user", "date")
    search_fields = ("post",)
    empty_value_display = "-empty-"


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
