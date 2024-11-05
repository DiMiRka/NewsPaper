from django.contrib import admin

from .models import Category, Post, PostCategory, SubscribersCategory


class CategoryAdmin(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CategoryAdmin,)
    list_display = ('name', 'author', 'article_or_news', 'rating', 'time_in')
    list_filter = ('name', 'author', 'article_or_news', 'category__name')
    search_fields = ('name', 'article_or_news', 'category__name', 'author__user__username')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(SubscribersCategory)
