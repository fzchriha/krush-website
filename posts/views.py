from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from collections import Counter
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import slugify
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

@login_required
def home_view(request):
    posts = Post.objects.filter(author=request.user)
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.name)
        newpost.save()
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'posts/home.html', context)

@login_required
def CreateCrush(request):
    posts = Post.objects.filter(author=request.user)
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        form.instance.author = request.user
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.name)
        newpost.save()
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'posts/create_crush.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['name', 'nickname', 'content']
    success_url = '/crush'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/crush'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDetailView(DetailView):
    model = Post

@login_required
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    user_posts = Post.objects.filter(author=request.user)
    posts = Post.objects.filter(tags=tag, author=request.user)
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'posts':posts,
    }
    return render(request, 'posts/home.html', context)

def statistics(request):
    traits = Counter()
    crushes =  Post.objects.filter(author=request.user)
    for crush in crushes:
        for trait in crush.tags.names():
            traits[trait] += 1
    context = {
        'traits': dict(traits)
    }
    
    return render(request, 'posts/statistics.html', context)