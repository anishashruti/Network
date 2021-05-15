from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class posts(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    authour=models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank=True,related_name='Post_likes')

    def __str__(self):
        return self.title

    def get_like_url(self):
        return reverse("post-like",kwargs={'pk':self.pk})

    # def get_api_like_url(self):
    #     return reverse("post-api-like")

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

