from django.db import models
from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager


# Create your models here.


# creating custom query manager
class PublishedManager(models.Manager):
     def get_queryset(self):
         return super(PublishedManager, self).get_queryset().filter(status='published')



class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
    unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
    choices=STATUS_CHOICES, default='draft')
    blog_image = models.ImageField( default = ' ', upload_to='images/')
    author_pic = models.ImageField(upload_to='images/', null=True)
    tags = TaggableManager()
    
    # query managers
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month, self.publish.day, self.slug])
    
    
    def  image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="80" height="80" />' % (self.author_pic))
    
    image_tag.allow_tags = True

    

    
    
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    
    
# comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email= models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'