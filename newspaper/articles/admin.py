from django.contrib import admin

# Register your models here.


from .models import *


class CommentInline(admin.TabularInline):  # new

    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):  # new

    inlines = [
        CommentInline,
    ]


admin.site.register(Article, ArticleAdmin)  # new


# admin.site.register(Article)
admin.site.register(Comment)
