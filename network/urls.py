from django.urls import path
from .import views
from .views import Post_list_view,PostDetailView,Post_create_view,Post_update_view,Post_delete_view,user_Post_list_view,PostLikeToggle,follow,following_posts

urlpatterns = [
    path('', Post_list_view.as_view(),name='blog-home'),
    path('user/<str:username>', user_Post_list_view.as_view(),name='user-post'),
    path('follow/<str:username>/', views.follow,name='follow'),
    path('unfollow/<str:username>/', views.unfollow,name='unfollow'),
    path('following/', views.following_posts,name='following'),
    path('post/<int:pk>/', PostDetailView.as_view(),name='post-detail'),
    path('post/<int:pk>/like', PostLikeToggle.as_view(),name='post-like'),
    path('post/NewPost/', Post_create_view.as_view(),name='post-create'),
    path('post/<int:pk>/update/', Post_update_view.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', Post_delete_view.as_view(),name='post-delete'),
    path('about/', views.about,name='blog-about'),
]