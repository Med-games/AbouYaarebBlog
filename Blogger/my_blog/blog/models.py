from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from embed_video.fields import EmbedVideoField
class video(models.Model):
    title=models.CharField(max_length=200)
    url=EmbedVideoField()
    def __str__(self) :
        return self.title
    

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    post_date=models.DateTimeField(default=timezone.now)
    Post_update=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,related_name='blog_posts')
    def total_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return self.title
    def get_absolute_url(self):
        return reverse('detail',args=[self.pk])
    class Meta:
        ordering=('-post_date',)

class Comment(models.Model):
    name=models.CharField(max_length=100, verbose_name='الاسم',default='مجهول')
    body=models.TextField(verbose_name='التعليق')
    comment_date=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    def __str__(self) -> str:
        return '  {} علق على تدوينة {}.'.format(self.name,self.post)
    class Meta:
        ordering=('-comment_date',)



