from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200, default=User, null=False, unique=True)
    email = models.EmailField()
    
    def __str__(self):
        return self.nickname
    
    
class Tag(models.Model):
    caption = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.caption


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.URLField(max_length = 400)
    slug = models.SlugField(max_length=200, unique=True, null=False, db_index=True)
    author = models.ForeignKey(Author, on_delete= models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

