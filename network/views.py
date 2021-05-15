from django.shortcuts import render,get_object_or_404,redirect
from .models import posts
import datetime
from django.db import IntegrityError
from django.contrib import messages
from users.models import followers
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    if request.method == 'GET':
        context={
            'posts':posts.objects.all(),
        }
        return render(request,'network/home.html',context)

def about(request):
    return render(request,'network/about.html',{'title':'About'})

def follow(request,username):
    source=username
    to_follow=request.user.username
    f=followers()
    f.source=User.objects.get(username=username)
    f.follower=request.user
    f.created = datetime.datetime.now()      
    try:
        f.save()  
        messages.success(request,'Successfully added to your following list')
        return redirect('blog-home')    
    except IntegrityError:
        messages.warning(request,'You are already following that user')
        return redirect('blog-home')
        
def unfollow(request,username):
    user=User.objects.get(username=username)
    f=followers.objects.filter(source=user,follower=request.user)
    f.delete()  
    messages.success(request,'Successfully removed from your following list')
    return redirect('blog-home')

def following_posts(request):
    qs=followers.objects.filter(follower=request.user)
    following=[item.source.pk for item in qs]
    all_posts=posts.objects.all()
    following_ppl_posts=[]
    for post in all_posts:
        if post.authour.pk in following:
            following_ppl_posts.append(post)       
    if len(following) != 0:
        context={
                "posts":following_ppl_posts
            }
    else:
        context={
                "msg":'Not following anyone yet!'
            }
    return render(request, "network/following_post.html",context)
    
class Post_list_view(ListView):
    model = posts

    template_name='network/home.html'
    context_object_name='posts'
    ordering=['-date']
    paginate_by=10

class user_Post_list_view(ListView):
    model = posts

    template_name='network/user_post.html'
    context_object_name='posts'
    paginate_by=3
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return posts.objects.filter(authour=user).order_by('date')

class PostDetailView(DetailView):
    model = posts

class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args ,**Kwargs):
        obj=get_object_or_404(posts,pk=self.kwargs.get('pk'))
        url_=obj.get_absolute_url()
        user =self.request.user
        if user in obj.likes.all():
            obj.likes.remove(user)
        else:
            obj.likes.add(user)
        return url_

class Post_delete_view(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = posts
    success_url='/'

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.authour:
            return True
        else:
            return False

class Post_create_view(LoginRequiredMixin, CreateView):
    model = posts
    fields=['title','content']

    def form_valid(self,form):
        form.instance.authour=self.request.user
        return super().form_valid(form)

class Post_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = posts
    fields=['title','content']

    def form_valid(self,form):
        form.instance.authour=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.authour:
            return True
        else:
            return False