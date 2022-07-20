from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    context={
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    # model tells listview what model to query
    model= Post
    template_name= 'blog/home.html'
    # looking for template with convention <app>/<model>_<viewtype>.html
    # we can set variable in listview and let class know that we want the variable to be known as posts instead
    context_object_name= 'posts'
    # ordering posts by date
    # ordering=['-date_posted']
    # we do pagination to add more pages and ensure website doesnt become slower
    paginate_by = 3

class UserPostListView(ListView): 
    model= Post
    template_name= 'blog/user_posts.html'
    context_object_name= 'posts'
    # ordering=['-date_posted']
    paginate_by = 2
    # in order to modify query set that list view returns 
    # we can override a method get_queryset and change the query set from there
    def get_queryset(self):
        user= get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        # we are overriding query that list view is maing so our order by will be overriden too

# class view for individual post(detailed view)
class PostDetailView(DetailView):
    # model tells listview what model to query
    model= Post

class PostCreateView(LoginRequiredMixin, CreateView):
    # model tells listview what model to query
    model= Post 
    fields= ['title', 'content']
    # to add author we have to override the form_valid method for the createview
    def form_valid(self,form):
        form.instance.author= self.request.user
        # take the instance and set author to current logged in user before submitting
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    # userpassestestmixin to ensure that a user cant change others posts
    # model tells listview what model to query
    model= Post 
    fields= ['title', 'content']
    # to add author we have to override the form_valid method for the createview
    def form_valid(self,form):
        form.instance.author= self.request.user
        # take the instance and set author to current logged in user before submitting
        return super().form_valid(form)

    def test_func(self):
        # in order to see if user passes certain condition
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    # model tells listview what model to query
    model= Post
    success_url='/'
    def test_func(self):
        # in order to see if user passes certain condition
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About Blog'})

# url patterns are directed to certain views which are these functions and 
# the views then handle the logic for the routes and thus render templates
# we convert this view to list view

# cant use login_required decorator with classes so we use LoginRequiredMixin