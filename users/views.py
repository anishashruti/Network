from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import followers
from .forms import UserRegisterationForms,UserUpdateForms,ProfileUserUpdateForms
# Create your views here.

def register(request):
    if request.method == 'POST':
        form=UserRegisterationForms(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            form.save()
            messages.success(request,'Your account has been created! You cannot Login')
            return redirect('login')
    else:
        form=UserRegisterationForms()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    followers_count=followers.objects.filter(source=request.user).count()
    print(followers_count)
    following_count=followers.objects.filter(follower=request.user).count()
    print(following_count)
    if request.method == 'POST':
        u_form=UserUpdateForms(request.POST,instance=request.user)
        p_form=ProfileUserUpdateForms(request.POST,request.FILES,  instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your account has been updated! ')
            return redirect('profile')
    else:
        u_form=UserUpdateForms(instance=request.user)
        p_form=ProfileUserUpdateForms(instance=request.user.profile)
    context={
            'u_form':u_form,
            'p_form':p_form,
            'followers_count':followers_count,
            'following_count':following_count,
        }
    return render(request,'users/profile.html',context)
