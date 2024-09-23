from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_template_names(self):
        if self.request.path == '/posts/search/':
            return 'search.html'
        return 'posts.html'


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.article_or_news = 'AR'
        post.save()
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts/')


class SubscribersList(ListView):
    model = Category
    template_name = 'subscribers.html'
    context_object_name = 'subscribers'

    def post(self, request, *args, **kwargs):
        category = self.request.POST.get('cat_name')
        request.session['sub_category'] = category
        return redirect('subscriber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_subscribers'] = self.request.user.category.all().values_list('name', flat=True)
        return context


@login_required
def subscribe_category(request):
    user = request.user
    subscriber = request.session['sub_category']
    category = Category.objects.get(name=subscriber)
    category.subscribers.add(user)
    return redirect('subscribers')

