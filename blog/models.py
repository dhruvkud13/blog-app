from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# orm= object relational mapping
# each class will be its own table in the database , each attribute will be a diff field in the database
class Post(models.Model):
    title= models.CharField(max_length=100)
    content= models.TextField()
    date_posted= models.DateTimeField(default= timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    # to delete posts oce user is deleted

    # migrations allow us to make changes to databse even after its created and has data

    def __str__(self):
        return self.title

    # to get url we use reverse function
    # reverse returns the full url to the route as a string
    # to find url of model object we need to create get_absolute_url method in model that returns path to any specific instance
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})