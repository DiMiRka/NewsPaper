from django.contrib import admin

from .models import Category, Post, PostCategory, SubscribersCategory


class CategoryAdmin(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CategoryAdmin,)


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(SubscribersCategory)
