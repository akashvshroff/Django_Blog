from django.shortcuts import render
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
import random


class PostListView(ListView):
    template_name = 'Blog/home.html'

    def get_queryset(self):
        self.query = self.request.GET.get('q')
        self.posts = Post.objects.all().order_by('-date_posted')
        if self.query:
            self.posts = []
            words = self.query.split()
            for word in words:
                self.posts.append(Post.objects.filter(
                    Q(title__icontains=word) | Q(
                        content__icontains=word)
                ).distinct())
            self.posts = list(set(self.posts))[0]
        else:
            self.query = 'Search...'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['posts'] = self.posts
        size = 5 if Post.objects.count() >= 5 else Post.objects.count()
        context['random_posts'] = random.sample(list(Post.objects.all()), size)
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        size = 5 if Post.objects.count() >= 5 else Post.objects.count()
        context['random_posts'] = random.sample(list(Post.objects.all()), size)
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    success_message = 'The post %(title)s has been deleted!'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        size = 5 if Post.objects.count() >= 5 else Post.objects.count()
        context['random_posts'] = random.sample(list(Post.objects.all()), size)
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # success_url = reverse_lazy('blog-home')
    success_message = '%(title)s has been added!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        size = 5 if Post.objects.count() >= 5 else Post.objects.count()
        context['random_posts'] = random.sample(list(Post.objects.all()), size)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_message = '%(title)s has been updated!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        size = 5 if Post.objects.count() >= 5 else Post.objects.count()
        context['random_posts'] = random.sample(list(Post.objects.all()), size)
        return context


def about(request):
    size = 5 if Post.objects.count() >= 5 else Post.objects.count()
    context = {
        'random_posts': random.sample(list(Post.objects.all()), size),
        'title': 'about'
    }
    return render(request, 'Blog/about.html', context)
