from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Friend

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'users/view_profile.html', args)

@login_required
def friends(request):
    users = User.objects.exclude(id=request.user.id)
    friend = get_object_or_404(Friend, from_user=request.user)
    friends = friend.to_user.all()
    context = {
        'users': users,
        'friends': friends,
    }
    return render(request, 'users/friends.html', context)

def update_friend(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.send_friend_request(request.user, new_friend)
    elif operation == 'remove':
        Friend.delete_friend(request.user, new_friend)

    users = User.objects.exclude(id=request.user.id)
    friend = Friend.objects.get(from_user=request.user)
    friends = friend.to_user.all()
    bestFriend = User.objects.get(pk=pk)
    context = {
        'users': users,
        'friends': friends,
        'bestFriend': bestFriend
    }
    return render(request, 'users/friends.html', context)
