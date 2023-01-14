from django.shortcuts import render
from blog.models import Post
# Create your views here.




def starting_page(request):
    posts = Post.objects.all().filter(status=1).order_by('-updated_on')[:3]
    return render(request, "blog/index.html", {"posts": posts})

def posts(request):
    posts = Post.objects.all().filter(status=1).order_by('-updated_on')
    return render(request, "blog/all-posts.html", {"posts": posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, "blog/post-detail.html", {"post": post})
