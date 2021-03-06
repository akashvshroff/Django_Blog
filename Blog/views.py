from django.shortcuts import render, get_object_or_404
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
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UserPostListView(ListView):
    model = Post
    template_name = 'Blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.posts = Post.objects.filter(author=user).order_by('-date_posted')
        return self.posts

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        paginator = Paginator(self.posts, 5)
        page = self.request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context['posts'] = page_object
        size = 5 if Post.objects.count() >= 5 else Post.objects.count()
        context['random_posts'] = random.sample(list(Post.objects.all()), size)
        return context


class PostListView(ListView):
    template_name = 'Blog/home.html'
    paginate_by = 5

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
        return self.posts

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['query'] = self.query
        paginator = Paginator(self.posts, 5)
        page = self.request.GET.get('page')
        try:
            # create Page object for the given page
            page_object = paginator.page(page)
        except PageNotAnInteger:
            # if page parameter in the query string is not available, return the first page
            page_object = paginator.page(1)
        except EmptyPage:
            # if the value of the page parameter exceeds num_pages then return the last page
            page_object = paginator.page(paginator.num_pages)

        context['posts'] = page_object
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
