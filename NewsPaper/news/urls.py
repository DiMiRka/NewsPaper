from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostsList, PostDetail, CreatePost, UpdatePost, DeletePost, upgrade_me, SubscribersList, subscribe_category

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsList.as_view(), name='post_search'),
    path('news/create/', CreatePost.as_view(), name='news_create'),
    path('articles/create/', CreatePost.as_view(), name='articles_create'),
    path('<int:pk>/news/update/', UpdatePost.as_view(), name='news_update'),
    path('<int:pk>/articles/update/', UpdatePost.as_view(), name='articles_update'),
    path('<int:pk>/news/delete/', DeletePost.as_view(), name='news_delete'),
    path('<int:pk>/articles/delete/', DeletePost.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('logout/', LogoutView.as_view(template_name='posts.html'), name='logout'),
    path('subscribers/', SubscribersList.as_view(), name='subscribers'),
    path('subscribers/subscriber/', subscribe_category, name='subscriber'),
]
