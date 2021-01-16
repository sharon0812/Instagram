from django.urls import path
# from django.conf.urls import url
from .views import *
from . import views


urlpatterns = [
    # path('', PostListView.as_view(), name='instaclone-index'),
    path('', posts_of_following_profiles, name='instaclone-index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('switch_follow/',follow_unfollow_profile , name='follow-unfollow-view'),
    path('<pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('<uuid:post_id>', views.post_detail, name='postdetail'),
    # path('<uuid:post_id>/like', views.like, name='likePost'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('post/<int:pk>/comment/', PostCommentView.as_view(), name='post-comment'),
    path('post/search/', views.search_results,  name='username'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    

]      