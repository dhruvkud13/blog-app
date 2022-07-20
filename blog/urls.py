from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    # pk is primary key to access post individually
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # template should be nameofmodel_form
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]
# class based have to be converted to views using as_view()
# use angular brackets to use parameter as url variable
# looking for template with convention <app>/<model>_<viewtype>.html

# post detail view takes us to specific post
# we have to create a url pattern that contains a variable(post/blog 1) type
# we have to create route where id of post is part of route