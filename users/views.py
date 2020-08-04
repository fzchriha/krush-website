from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, FriendRequest

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('account_login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def settings(request):
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

    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }

    return render(request, 'users/settings.html', context)


User = get_user_model()

def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
    context = {
        'users': users,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }
    return render(request, "users/friends.html", context)

def send_friend_request(request, id):
        user = get_object_or_404(User, id=id)
        frequest, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=user)
        return HttpResponseRedirect('/friends')

def cancel_friend_request(request, id):
        user = get_object_or_404(User, id=id)
        frequest = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.delete()
        return HttpResponseRedirect('/friends')

def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    return HttpResponseRedirect('/profile')

def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/{}'.format(request.user.profile.slug))

def profile(request):
    p = Profile.objects.filter(user=request.user).first()
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)

    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
            from_user=request.user).filter(to_user=p.user)) == 1:
                button_status = 'friend_request_sent'

    context = {
        'u': u,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }
    return render(request, "users/profile.html", context)
def profile_view(request, pk=None):
    p = Profile.objects.get(pk=pk)
    u = p.user
    
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)

    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
            from_user=request.user).filter(to_user=p.user)) == 1:
                button_status = 'friend_request_sent'
    print(u)
    print(request.user)
    print(u == request.user)
    print(friends)
    print(sent_friend_requests)
    context = {
        'u': u,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }

    return render(request, "users/profile.html", context)




