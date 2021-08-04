from django.shortcuts import render, get_object_or_404
from .models import Post
from users.models import Profile, FriendRequest
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
# This method displays the crushes in the home page
# PS: even though friend requests are in the context it is not used yet
# I was counting on diplaying crushes in my friends pages if we are friends (feature no added yet)
@login_required
def crush(request):
    posts = Post.objects.filter(author=request.user)
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.name)
        newpost.save()
        form.save_m2m()
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
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

# Update the crush's profile
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

# Delete the crush's profile
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

# Method is used to enable clicking on a specific tag (trait) and it filters the crushes who have that trait
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

# Function to get the analysis of the crushes traits
# Checkout this article I wrote to understand more how the report is generated
# https://medium.com/@fatimazahrachriha/combine-django-taggit-and-chartjs-85de844de30c
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
