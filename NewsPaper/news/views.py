from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .filters import PostFilter
from .forms import PostForm


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
        return context

    def get_template_names(self):
        if self.request.path == '/posts/search/':
            return 'search.html'
        return 'posts.html'


class CreatePost(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.article_or_news = 'AR'
        post.save()
        return super().form_valid(form)


class UpdatePost(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class DeletePost(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
