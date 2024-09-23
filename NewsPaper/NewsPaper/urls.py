from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import IndexView, BaseRegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('posts/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', IndexView.as_view()),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='posts.html')),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html')),
]
